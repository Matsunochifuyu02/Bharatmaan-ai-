import requests
import sqlite3

API_KEY = "api_key"

# ===== DATABASE SETUP =====
conn = sqlite3.connect("memory.db")
cursor = conn.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS chat (role TEXT, content TEXT)")
conn.commit()

# ===== CHAT FUNCTION =====
def chat():
    print("🇮🇳 Bharatmaan AI started! (type 'exit' to stop)\n")

    while True:
        user = input("You: ")

        if user.lower() == "exit":
            print("AI: Bye! 👋")
            break

        # clean input
        user = user.replace('"', '\\"')

        # SAVE USER MESSAGE
        cursor.execute("INSERT INTO chat VALUES (?, ?)", ("user", user))
        conn.commit()

        # LOAD LAST 10 MESSAGES
        cursor.execute("SELECT role, content FROM chat ORDER BY ROWID DESC LIMIT 10")
        rows = cursor.fetchall()

        chat_history = []
        for r in reversed(rows):
            chat_history.append({"role": r[0], "content": r[1]})

        # ===== SYSTEM PROMPT (CLEAN) =====
        system_prompt = "You are Bharatmaan AI, a smart and helpful AI assistant created by Krushna. Speak in simple and clear English. Be respectful, calm, and supportive. Do not use slang. Keep answers short and meaningful. Understand user intent even if there are spelling mistakes. If something is unclear, ask a simple question. Give practical and realistic solutions, especially for users with low budget. Maintain a professional but friendly tone.If someone asks who created you, clearly say: 'I was created by Krushna Jawale.' Don' tell them always that you were created by krushna jawale if they ask or if they say that tell me about your self that time only tell that you were created by Krushna Jawale."

        messages = [{"role": "system", "content": system_prompt}] + chat_history

        # ===== API DATA =====
        data = {
            "model": "meta-llama/llama-3-8b-instruct",
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0.6
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        try:
            res = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                json=data,
                headers=headers
            )

            result = res.json()

            if "choices" in result:
                reply = result["choices"][0]["message"]["content"]
                print("AI:", reply, "\n")

                # SAVE AI REPLY
                cursor.execute("INSERT INTO chat VALUES (?, ?)", ("assistant", reply))
                conn.commit()
            else:
                print("API Error:", result)

        except Exception as e:
            print("Error:", e)

# ===== RUN =====
chat()