# 프로젝트: 토익스피킹 독학 웹페이지

React + Vite + TypeScript로 토익스피킹 학습 웹앱을 만들어줘.

## 기술 스택
- React 18
- Vite
- Tailwind CSS
- Upstage Solar LLM API

## 상세 구현 요구사항

### 1. 환경변수 설정 (.env.local)
```env
VITE_UPSTAGE_API_KEY=your_api_key_here
VITE_UPSTAGE_API_URL=https://api.upstage.ai/v1/solar/chat/completions
```

### 2. Upstage API 호출 로직 (src/services/upstageAPI.js)
```javascript
/**
 * Upstage Solar LLM API 호출 함수
 * @param {string} systemPrompt - 시스템 프롬프트 (역할 정의)
 * @param {string} userPrompt - 사용자 프롬프트 (문제+답변)
 * @returns {Promise<string>} - AI 피드백 텍스트
 */
export async function getFeedback(systemPrompt, userPrompt) {
  const response = await fetch(import.meta.env.VITE_UPSTAGE_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${import.meta.env.VITE_UPSTAGE_API_KEY}`
    },
    body: JSON.stringify({
      model: 'solar-1-mini-chat', // 또는 solar-pro
      messages: [
        { role: 'system', content: systemPrompt },
        { role: 'user', content: userPrompt }
      ],
      temperature: 0.7,
      max_tokens: 2000
    })
  });
  
  const data = await response.json();
  return data.choices[0].message.content;
}
```

### 3. 프롬프트 생성 유틸 (src/utils/promptBuilder.js)
```javascript
/**
 * One-shot 예시를 포함한 시스템 프롬프트 생성
 * @param {string} examplesText - feedback-examples.txt 내용
 * @returns {string} - 완성된 시스템 프롬프트
 */
export function buildSystemPrompt(examplesText) {
  return `당신은 토익스피킹 전문 튜터입니다.
목표: 학생이 IH 레벨 (130점)에 도달하도록 구체적이고 실용적인 피드백 제공

[One-shot 학습 예시]
${examplesText}

위 예시의 피드백 스타일을 참고하여:
1. 답변의 강점 1-2가지 짚어주기
2. 문법/어휘/구조 개선점 구체적으로 제시
3. IH 수준 답변으로 개선하는 방법 단계별 안내
4. 친절하지만 직설적인 어조 유지

응답 형식:
## 강점
- (강점 1-2개)

## 개선 필요
- (문법/어휘/구조 각각)

## IH 도달 전략
- (구체적 액션 아이템)

## 수정 예시
- (개선된 문장 샘플)
`;
}

/**
 * 사용자 프롬프트 생성
 * @param {string} problem - 현재 문제
 * @param {string} userAnswer - 학생 답변
 * @returns {string}
 */
export function buildUserPrompt(problem, userAnswer) {
  return `[문제]
${problem}

[학생 답변]
${userAnswer}

위 답변을 IH 레벨 기준으로 분석하고 피드백해주세요.`;
}
```

### 4. 데이터 로더 (src/services/dataLoader.js)
```javascript
/**
 * public 폴더의 txt 파일 읽기
 * @param {string} filename - 파일명 (예: 'problems.txt')
 * @returns {Promise<string>} - 파일 내용
 */
export async function loadTextFile(filename) {
  const response = await fetch(`/${filename}`);
  if (!response.ok) {
    throw new Error(`파일 로드 실패: ${filename}`);
  }
  return await response.text();
}

/**
 * problems.txt에서 문제 파싱
 * 형식: "Q1. 문제내용\n\nQ2. ..." 가정
 * @param {string} text - 전체 텍스트
 * @returns {Array<{id: number, question: string}>}
 */
export function parseProblems(text) {
  // 실제 파일 형식에 맞게 수정 필요
  const problems = text
    .split(/Q\d+\./)
    .filter(Boolean)
    .map((q, idx) => ({
      id: idx + 1,
      question: q.trim()
    }));
  
  return problems;
}
```

### 5. 메인 컴포넌트 (src/App.jsx)
```javascript
import { useState, useEffect } from 'react';
import ProblemCard from './components/ProblemCard';
import AnswerTextarea from './components/AnswerTextarea';
import FeedbackPanel from './components/FeedbackPanel';
import LoadingSpinner from './components/LoadingSpinner';
import { loadTextFile, parseProblems } from './services/dataLoader';
import { getFeedback } from './services/upstageAPI';
import { buildSystemPrompt, buildUserPrompt } from './utils/promptBuilder';

function App() {
  // 상태 관리
  const [problems, setProblems] = useState([]); // 문제 리스트
  const [currentProblem, setCurrentProblem] = useState(null); // 현재 문제
  const [userAnswer, setUserAnswer] = useState(''); // 사용자 답변
  const [feedback, setFeedback] = useState(''); // AI 피드백
  const [isLoading, setIsLoading] = useState(false); // 로딩 상태
  const [examplesText, setExamplesText] = useState(''); // one-shot 예시

  // 초기 데이터 로드
  useEffect(() => {
    async function loadData() {
      try {
        // 문제 파일 로드
        const problemsText = await loadTextFile('problems.txt');
        const parsedProblems = parseProblems(problemsText);
        setProblems(parsedProblems);
        
        // 랜덤 문제 선택
        const randomProblem = parsedProblems[
          Math.floor(Math.random() * parsedProblems.length)
        ];
        setCurrentProblem(randomProblem);
        
        // 피드백 예시 로드
        const examples = await loadTextFile('feedback-examples.txt');
        setExamplesText(examples);
      } catch (error) {
        console.error('데이터 로드 실패:', error);
        alert('파일을 불러올 수 없습니다. public 폴더를 확인하세요.');
      }
    }
    
    loadData();
  }, []);

  // 피드백 받기 버튼 클릭 핸들러
  async function handleGetFeedback() {
    if (!userAnswer.trim()) {
      alert('답변을 먼저 입력해주세요.');
      return;
    }
    
    setIsLoading(true);
    setFeedback('');
    
    try {
      // 프롬프트 생성
      const systemPrompt = buildSystemPrompt(examplesText);
      const userPrompt = buildUserPrompt(
        currentProblem.question,
        userAnswer
      );
      
      // API 호출
      const result = await getFeedback(systemPrompt, userPrompt);
      setFeedback(result);
    } catch (error) {
      console.error('피드백 생성 실패:', error);
      alert('피드백을 받는 중 오류가 발생했습니다.');
    } finally {
      setIsLoading(false);
    }
  }

  // 다음 문제로 이동
  function handleNextProblem() {
    const randomProblem = problems[
      Math.floor(Math.random() * problems.length)
    ];
    setCurrentProblem(randomProblem);
    setUserAnswer('');
    setFeedback('');
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8 px-4">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold text-center mb-8">
          토익스피킹 IH 독학 튜터
        </h1>
        
        {currentProblem && (
          <>
            <ProblemCard problem={currentProblem} />
            
            <AnswerTextarea 
              value={userAnswer}
              onChange={setUserAnswer}
            />
            
            <div className="flex gap-4 mb-8">
              <button
                onClick={handleGetFeedback}
                disabled={isLoading}
                className="flex-1 bg-blue-600 text-white py-3 rounded-lg
                         hover:bg-blue-700 disabled:bg-gray-400"
              >
                {isLoading ? '분석 중...' : '피드백 받기'}
              </button>
              
              <button
                onClick={handleNextProblem}
                className="px-6 bg-gray-200 rounded-lg hover:bg-gray-300"
              >
                다음 문제
              </button>
            </div>
            
            {isLoading && <LoadingSpinner />}
            
            {feedback && <FeedbackPanel feedback={feedback} />}
          </>
        )}
      </div>
    </div>
  );
}

export default App;
```

### 6. 컴포넌트 예시

**ProblemCard.jsx**
```javascript
export default function ProblemCard({ problem }) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-md mb-6">
      <div className="text-sm text-gray-500 mb-2">
        Question {problem.id}
      </div>
      <p className="text-lg whitespace-pre-wrap">
        {problem.question}
      </p>
    </div>
  );
}
```

**AnswerTextarea.jsx**
```javascript
export default function AnswerTextarea({ value, onChange }) {
  return (
    <div className="mb-6">
      <label className="block text-sm font-medium mb-2">
        답변 (영어로 작성)
      </label>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="답변을 입력하세요..."
        className="w-full h-48 p-4 border rounded-lg resize-none
                   focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      />
      <div className="text-sm text-gray-500 mt-2">
        글자 수: {value.length}
      </div>
    </div>
  );
}
```

**FeedbackPanel.jsx**
```javascript
export default function FeedbackPanel({ feedback }) {
  return (
    <div className="bg-green-50 p-6 rounded-lg border-l-4 border-green-500">
      <h2 className="text-xl font-bold mb-4">📝 피드백</h2>
      <div className="prose prose-sm max-w-none whitespace-pre-wrap">
        {feedback}
      </div>
    </div>
  );
}
```

## 실행 방법
```bash
# 프로젝트 생성
npm create vite@latest toeic-tutor -- --template react

# 의존성 설치
cd toeic-tutor
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# 개발 서버 실행
npm run dev
```

## 중요 체크리스트
- [ ] public/problems.txt 파일 배치
- [ ] public/feedback-examples.txt 파일 배치
- [ ] .env.local에 Upstage API 키 설정
- [ ] txt 파일 형식에 맞게 parseProblems() 수정
- [ ] Tailwind CSS 설정 (tailwind.config.js)