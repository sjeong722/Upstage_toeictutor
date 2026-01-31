export interface Question {
    id: number;
    type: string;
    question: string;
    context?: string; // For things like tables or image descriptions
}

export const questions: Question[] = [
    {
        id: 1,
        type: "Read a text aloud",
        question: "Read the following text aloud:\n\nThe King Community Center is recruiting volunteers.\n\nIf you are looking for a way to get more involved in the community, now is your chance.\n\nThis year volunteers will be asked to tutor students, assist the elderly, and help organize social events and special projects.\n\nVisit our office today to fill out a volunteer form."
    },
    {
        id: 3,
        type: "Describe a picture",
        question: "Describe the picture in detail.",
        context: "[Image Context: Two women with blonde hair looking at a laptop screen while sitting at a table. On the right, a man in a black suit is entering a way. There are potted plants in the middle.]"
    },
    {
        id: 5,
        type: "Respond to questions",
        question: "When was the last time you cooked, and what did you make?"
    },
    {
        id: 6,
        type: "Respond to questions",
        question: "Do you plan to buy a new cooking tool in the near future? Why or Why not?"
    },
    {
        id: 7,
        type: "Respond to questions",
        question: "Do you think reading a cookbook is a good way to learn how to cook? Why or Why not?"
    },
    {
        id: 8,
        type: "Respond to questions using information provided",
        question: "Where will the conference be held, and how much is the participation fee?",
        context: "[Schedule Information]\nEvent: Annual Tech Conference\nLocation: Hilltop Convention Center\nParticipation Fee: $50"
    },
    {
        id: 9,
        type: "Respond to questions using information provided",
        question: "What should I do about lunch? Do I need to prepare my own meal?",
        context: "[Schedule Information]\nLunch: Provided by Green Trail Cafe"
    },
    {
        id: 11,
        type: "Express an opinion",
        question: "If you receive a gift that you don't really want to keep, do you think it's okay to give it to someone else? Why or why not? Give reasons or examples to support your opinion."
    }
];
