from ai.chatbot import ask_finance


def explain_stock(ticker, overview, pros, cons):

    prompt = f"""
You are a professional financial analyst.

Analyze the company {ticker} based on the following data:

Overview:
{overview}

Pros:
{pros}

Cons:
{cons}

Give:
1. Business summary
2. Financial strength
3. Risks
4. Investment outlook

Keep it simple and insightful.
"""

    return ask_finance(prompt)