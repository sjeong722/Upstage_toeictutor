export async function getFeedback(systemPrompt: string, userPrompt: string): Promise<string> {
    const apiKey = import.meta.env.VITE_UPSTAGE_API_KEY;
    const apiUrl = import.meta.env.VITE_UPSTAGE_API_URL || 'https://api.upstage.ai/v1/solar/chat/completions';

    if (!apiKey) {
        throw new Error('Upstage API Key is missing. Please check .env.local');
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`
            },
            body: JSON.stringify({
                model: 'solar-1-mini-chat',
                messages: [
                    { role: 'system', content: systemPrompt },
                    { role: 'user', content: userPrompt }
                ],
                temperature: 0.7,
                max_tokens: 1500
            })
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(`API Error: ${response.status} ${JSON.stringify(errorData)}`);
        }

        const data = await response.json();
        return data.choices[0].message.content;
    } catch (error) {
        console.error('Failed to fetch feedback:', error);
        throw error;
    }
}
