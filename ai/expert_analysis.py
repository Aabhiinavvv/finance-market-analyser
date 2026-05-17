from ai.chatbot import ask_finance

def analyze_event(news):

    prompt = f"""
You are a financial intelligence analyst.

Analyze the following news from four expert perspectives.

News:
{news}

Respond using EXACTLY the following format:

Economist Perspective:
(4-5 concise sentences)

Political Analyst Perspective:
(4-5 concise sentences)

Market Strategist Perspective:
(4-5 concise sentences)

Investor Conclusion:
(3-4 concise sentences)

Keep the total answer under 600 tokens and ensure ALL sections are completed.
"""
    
    

    result = ask_finance(prompt)

    return result