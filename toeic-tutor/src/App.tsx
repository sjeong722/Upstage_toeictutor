import { useState } from 'react';
import { questions, Question } from './data/questions';
import { getFeedback } from './services/upstage';
import { buildSystemPrompt, buildUserPrompt } from './utils/prompt';
import ReactMarkdown from 'react-markdown';

function App() {
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [userAnswer, setUserAnswer] = useState('');
    const [feedback, setFeedback] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const currentQuestion = questions[currentQuestionIndex];

    const handleNext = () => {
        setCurrentQuestionIndex((prev) => (prev + 1) % questions.length);
        setUserAnswer('');
        setFeedback('');
    };

    const handlePrev = () => {
        setCurrentQuestionIndex((prev) => (prev - 1 + questions.length) % questions.length);
        setUserAnswer('');
        setFeedback('');
    };

    const handleSubmit = async () => {
        if (!userAnswer.trim()) {
            alert('Please enter your answer first.');
            return;
        }

        setIsLoading(true);
        setFeedback('');

        try {
            const systemPrompt = buildSystemPrompt();
            const userPrompt = buildUserPrompt(currentQuestion.question, currentQuestion.context, userAnswer);

            const response = await getFeedback(systemPrompt, userPrompt);
            setFeedback(response);
        } catch (error) {
            alert('Error fetching feedback. Please check your API key and try again.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gray-100 py-10 px-4 font-sans">
            <div className="max-w-4xl mx-auto space-y-8">

                {/* Header */}
                <div className="text-center">
                    <h1 className="text-4xl font-extrabold text-blue-800 mb-2">TOEIC Speaking Tutor</h1>
                    <p className="text-gray-600">Practice with real exam questions and get AI feedback to reach IH/AL.</p>
                </div>

                {/* Question Card */}
                <div className="bg-white rounded-2xl shadow-xl overflow-hidden border border-gray-200">
                    <div className="bg-blue-600 px-6 py-4 flex justify-between items-center text-white">
                        <h2 className="font-bold text-lg">Question {currentQuestion.id}</h2>
                        <span className="text-blue-100 text-sm">{currentQuestion.type}</span>
                    </div>
                    <div className="p-8">
                        <p className="text-xl text-gray-800 whitespace-pre-wrap leading-relaxed">
                            {currentQuestion.question}
                        </p>
                        {currentQuestion.context && (
                            <div className="mt-6 bg-gray-50 p-4 rounded-lg border-l-4 border-blue-400">
                                <h3 className="text-sm font-bold text-gray-500 mb-2 uppercase tracking-wide">Context Info</h3>
                                <p className="whitespace-pre-wrap text-gray-700 font-mono text-sm">
                                    {currentQuestion.context}
                                </p>
                            </div>
                        )}
                    </div>

                    {/* Navigation */}
                    <div className="px-6 py-4 bg-gray-50 border-t border-gray-100 flex justify-between">
                        <button
                            onClick={handlePrev}
                            className="text-gray-500 hover:text-blue-600 font-medium transition-colors"
                        >
                            ← Previous
                        </button>
                        <button
                            onClick={handleNext}
                            className="text-gray-500 hover:text-blue-600 font-medium transition-colors"
                        >
                            Next Question →
                        </button>
                    </div>
                </div>

                {/* Interaction Area */}
                <div className="grid md:grid-cols-2 gap-6">

                    {/* Input Section */}
                    <div className="space-y-4">
                        <div className="bg-white rounded-xl shadow-md p-6">
                            <label className="block text-gray-700 font-bold mb-3">Your Answer</label>
                            <textarea
                                value={userAnswer}
                                onChange={(e) => setUserAnswer(e.target.value)}
                                placeholder="Type your answer here (as if you are speaking)..."
                                className="w-full h-64 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none transition-shadow"
                            />
                            <div className="mt-4 flex justify-end">
                                <button
                                    onClick={handleSubmit}
                                    disabled={isLoading}
                                    className="bg-blue-600 text-white px-8 py-3 rounded-lg font-bold shadow-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all transform hover:-translate-y-0.5"
                                >
                                    {isLoading ? 'Analyzing...' : 'Get AI Feedback'}
                                </button>
                            </div>
                        </div>
                    </div>

                    {/* Feedback Section */}
                    <div className="space-y-4">
                        <div className={`bg-white rounded-xl shadow-md p-6 h-full min-h-[400px] border-2 ${feedback ? 'border-green-400' : 'border-transparent'}`}>
                            <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
                                <span>AI Tutor Feedback</span>
                                {feedback && <span className="ml-2 text-green-500 text-sm">● Active</span>}
                            </h3>

                            {isLoading ? (
                                <div className="h-64 flex flex-col items-center justify-center text-gray-400">
                                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                                    <p>Analyzing your grammar and delivery...</p>
                                </div>
                            ) : feedback ? (
                                <div className="prose prose-blue max-w-none text-sm overflow-y-auto max-h-[500px] bg-gray-50 p-4 rounded-lg">
                                    <ReactMarkdown>{feedback}</ReactMarkdown>
                                </div>
                            ) : (
                                <div className="h-64 flex items-center justify-center text-gray-400 text-center px-8">
                                    <p>Submit your answer to receive detailed feedback on valid IH/AL level strategies.</p>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default App;
