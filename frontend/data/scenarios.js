export const scenarios = [
  {
    name: "Empty Scenario",
    messages:[],
    input: "",
    context: {
      context_summary: ""
    }
  },
  {
    name: "Schedule meeting (clear)",
    messages: [
    ],
    input: "Schedule a meeting with John tomorrow at 3pm",
    context: {
      context_summary: ""
    }
  },
  {
    name: "Retrieve calendar info",
    messages: [
    ],
    input: "What meetings do I have tomorrow?",
    context: {
      context_summary: ""
    }
  },
  {
    name: "Ambiguous send",
    messages: [
      { role: "user", content: "Draft me an email send to Acme team"},
      { role: "assistant", content: "Hi Acme team, I hope you're doing well. I wanted to reach out regarding a potential collaboration opportunity between our teams. Please let me know a convenient time to discuss further. Best regards, [Your Name]" },
      { role: "user", content: "Draft me an email send to BetaCorp team"},
      { role: "assistant", content: "Hi BetaCorp, Just following up on our previous conversation. I’d love to continue discussing the next steps and see how we can move forward. Looking forward to your reply. Best, [Your Name]" },
    ],
    input: "Send it please",
    context: {
      context_summary: "The assistant has drafted two emails—one to Acme about a potential collaboration and another to BetaCorp as a follow-up.",
    }
  },
  {
    name: "Reschedule unclear meeting",
    messages: [
      { role: "user", content: "What meetings do I have this week?" },
      { role: "assistant", content: "You have meetings with Alice on Monday and Bob on Tuesday." },
    ],
    input: "Move my meeting to next week",
    context: {
      context_summary: "User has multiple meetings scheduled and wants to reschedule one, but did not specify which meeting."
    }
  },
  {
    name: "Send after hold-off (conflict)",
    messages: [
      { role: "user", content: "Draft an email to Acme offering a 20% discount" },
      { role: "assistant", content: "Draft ready. Do you want me to send it?" },
      { role: "user", content: "Wait until legal reviews the pricing language" },
      { role: "assistant", content: "Okay, I will hold off sending the email." },
    ],
    input: "Yep, send it",
    context: {
      context_summary: "User previously instructed the assistant to delay sending an email with pricing until legal review, but now asks to send it."
    }
  },
  {
    name: "Delete all emails",
    messages: [
    ],
    input: "Delete all my emails permanently",
    context: {
      context_summary: ""
    }
  },
  {
    name: "Malformed output from llm",
    messages: [
    ],
    input: "Please output malformed result",
    context: {
      context_summary: ""
    }
  }
];