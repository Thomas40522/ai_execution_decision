INTENT_DEFINITIONS = {
    "SEND_EMAIL": {
        "description": "User wants to draft, send, or reply to an email.",
        "examples": [
            "send the email",
            "draft an email to Acme",
            "reply to that message"
        ],
        "notes": [
            "Often involves recipients",
            "High risk if external communication"
        ]
    },

    "SCHEDULE_EVENT": {
        "description": "User wants to create a new meeting or calendar event.",
        "examples": [
            "schedule a meeting with John",
            "set up a call tomorrow"
        ],
        "notes": [
            "Requires time and participants"
        ]
    },

    "RESCHEDULE_EVENT": {
        "description": "User wants to modify the time of an existing event.",
        "examples": [
            "move my meeting to next week",
            "reschedule the call"
        ],
        "notes": [
            "Requires identifying which event"
        ]
    },

    "DELETE_ITEM": {
        "description": "User wants to delete or remove something.",
        "examples": [
            "delete this email",
            "remove the event"
        ],
        "notes": [
            "May be irreversible"
        ]
    },

    "UPDATE_ITEM": {
        "description": "User wants to modify an existing item.",
        "examples": [
            "update the meeting time",
            "change the email content"
        ]
    },

    "RETRIEVE_INFO": {
        "description": "User is asking for information.",
        "examples": [
            "what meetings do I have tomorrow?",
            "show my emails"
        ],
        "notes": [
            "Low risk"
        ]
    },

    "GENERAL_CHAT": {
        "description": "Casual conversation or unclear intent.",
        "examples": [
            "hello",
            "how are you",
            "can you help me?"
        ]
    }
}

ISSUE_DEFINITIONS = {
    "AMBIGUOUS_TARGET": {
        "description": "The user refers to something unclear (e.g., 'it', 'that').",
        "examples": [
            "send it",
            "delete that"
        ],
        "trigger": "missing clear reference",
        "do not trigger": "user input with clear name that appears in the context"
    },

    "MISSING_PARAMETERS": {
        "description": "Required information is missing.",
        "examples": [
            "schedule a meeting",
            "send an email"
        ],
        "trigger": "no time, no recipient",
        "do not trigger": "user input contains specific name and clear time that appears in the context"
    },

    "CONFLICTING_CONTEXT": {
        "description": "The request contradicts earlier instructions.",
        "examples": [
            "I need to wait for authorization to send it → without authorization, just said send it",
            "wait to send → later send it"
        ],
        "trigger": "history contains opposite instruction"
    },

    "HIGH_RISK_ACTION": {
        "description": "Action has external or significant impact.",
        "examples": [
            "send email",
            "share file"
        ],
        "trigger": "affects external parties or critical data"
    },

    "IRREVERSIBLE_ACTION": {
        "description": "Action cannot be undone.",
        "examples": [
            "delete all emails",
            "permanently remove data"
        ],
        "trigger": "destructive operations"
    },

    "UNAUTHORIZED_ACTION": {
        "description": "Action is unsafe or not allowed.",
        "examples": [
            "send confidential data externally"
        ],
        "trigger": "perform system level change"
    },

    "LOW_CONFIDENCE_INTENT": {
        "description": "User intent is unclear or vague.",
        "examples": [
            "do it",
            "help me with that"
        ]
    }
}

DECISION_DEFINITIONS = {

    "EXECUTE_SILENTLY": {
        "description": "Execute the action without notifying the user.",
        "when_to_use": [
            "Low risk action",
            "Fully specified intent",
            "No ambiguity or missing parameters",
            "Action is reversible or harmless",
            "Action is just asking to wait"
        ],
        "examples": [
            "delete a draft email",
            "mark email as read"
        ],
        "avoid_if": [
            "Any risk is present",
            "User intent is unclear",
            "External impact exists"
        ]
    },

    "EXECUTE_AND_NOTIFY": {
        "description": "Execute the action and inform the user after completion.",
        "when_to_use": [
            "Low to moderate risk action",
            "Intent is clear and complete",
            "User expects a result (information retrieval or scheduling)"
        ],
        "examples": [
            "schedule a meeting",
            "retrieve calendar info"
        ],
        "avoid_if": [
            "High risk or irreversible action",
            "Ambiguity exists"
        ]
    },

    "CONFIRM_BEFORE": {
        "description": "Ask the user for confirmation before executing the action.",
        "when_to_use": [
            "High risk action",
            "Irreversible action",
            "Conflicting context exists",
            "Action affects external parties"
        ],
        "examples": [
            "send an email",
            "delete all emails"
        ],
        "avoid_if": [
            "Action is clearly safe and low risk"
        ]
    },

    "ASK_CLARIFICATION": {
        "description": "Ask a clarifying question before taking action.",
        "when_to_use": [
            "Ambiguous target (e.g., 'send it')",
            "Missing required parameters",
            "Low confidence in intent"
        ],
        "examples": [
            "Which email should I send?",
            "What time should I schedule the meeting?"
        ],
        "avoid_if": [
            "Intent is fully clear and complete"
        ]
    },

    "REFUSE": {
        "description": "Refuse to perform the action due to safety or policy concerns.",
        "when_to_use": [
            "Unauthorized or unsafe action",
            "Potential policy violation",
            "Extremely high risk with no safe fallback"
        ],
        "examples": [
            "sending confidential data externally",
            "performing restricted operations"
        ],
        "avoid_if": [
            "A safe alternative (clarification or confirmation) is possible"
        ]
    }
}
