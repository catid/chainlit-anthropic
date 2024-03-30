import os
import anthropic
import chainlit as cl
from chainlit.playground.providers import Anthropic

c = anthropic.AsyncAnthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@cl.on_chat_start
async def start_chat():
    cl.user_session.set(
        "prompt_history",
        "",
    )
    await cl.Avatar(
        name="Claude",
        url="https://www.anthropic.com/images/icons/apple-touch-icon.png",
    ).send()


@cl.step(name="Claude", type="llm", root=True)
async def call_claude(query: str):
    prompt_history = cl.user_session.get("prompt_history")
    messages = cl.user_session.get("messages")

    if not messages:
        messages = []

    prompt = f"{prompt_history}{anthropic.HUMAN_PROMPT}{query}{anthropic.AI_PROMPT}"

    settings = {
        "max_tokens": 1024,
        "model": "claude-3-opus-20240229",
        "system": "You are a helpful and knowledgeable C++ optimization assistant.  You mainly write C++ header/source files with CMakeLists.txt build scripts.  You always write the most optimized code, leveraging multi-threading and SIMD where possible.",
    }

    new_message = [
        {
            "role": "user",
            "content": query
        }
    ]

    messages += new_message
    print(f"Messages: {messages}")

    ai_text = ""

    async with c.messages.stream(
        messages=messages,
        **settings,
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)
            ai_text += text
            await cl.context.current_step.stream_token(text)
        print()

    # Only after accumulating the complete AI response, append it to `messages` and `prompt_history`.
    ai_message = [
        {
            "role": "assistant",
            "content": cl.context.current_step.output
        }
    ]

    messages += ai_message

    cl.user_session.set("messages", messages)

    # Update the `cl.context.current_step.generation` with the final `ai_text`.
    cl.context.current_step.generation = cl.CompletionGeneration(
        formatted=prompt,
        completion=cl.context.current_step.output,
        settings=settings,
        provider=Anthropic.id,
    )

    cl.user_session.set("prompt_history", prompt + cl.context.current_step.output)


@cl.on_message
async def chat(message: cl.Message):
    await call_claude(message.content)
