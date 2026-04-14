# # magic mathods and magic attributes 




# # instance methods and instance attributes  instance class

# class Person:
#     name : str
#     age : int
#     grade : str

#     # Magic method __init__ is used to initialize the instance attributes
    
#     def __init__(self , name : str , age : int , grade : str):
#         self.name = name
#         self.age = age
#         self.grade = grade
    
# p1 = Person("John" , 20 , "A")
# # print(p1.name)
# # print(p1.age)
# # print(p1.grade)



# # / magic attributes 

# def my_function():
#     """this is my function  """
#     print("Hello World")

# print(my_function.__doc__) # this will print the docstring of the function

import os 
import sys
import asyncio
from shared.models.ollama_provider import get_model
print(os.path.join(os.path.dirname(__file__), "..",".."))

from agents import Agent , Runner , function_tool
from agents import input_guardrail, output_guardrail , GuardrailFunctionOutput

@function_tool
def great(nmae: str)  -> str:
    """Great a person by name."""
    return f"Hello {os.name}: Welcome to Agentic AI hub!"


guardrail_agent = Agent(
    name = "guardrail agent",
    instructions="you are a helpful assistant that can answer questions and perform tasks for the user",
    model=get_model()

)



@input_guardrail
async def check_input(ctx, agent , input ) -> GuardrailFunctionOutput:
    """Check if the user input is valid."""
    if len(user_input) < 5:
        return GuardrailFunctionOutput(
            is_valid=False,
            message="Input is too short. Please provide more details."
        )
    return GuardrailFunctionOutput(
        is_valid=True,
        message="Input is valid."
    )

@output_guardrail
async def check_output(ctx, agent , output ) -> GuardrailFunctionOutput:
    """Ensure output don't contain any sensitive information."""
    # Example check (replace with actual sensitive information detection logic)
    if "secret" in output.lower():
        return GuardrailFunctionOutput(
            is_valid=False,
            message="Output contains sensitive information."
        )
    return GuardrailFunctionOutput(
        is_valid=True,
        message="Output is valid."
    )

agent = Agent(
    name = "my agent",
    instructions="you are a helpful assistant that can answer questions and perform tasks for the user",
    model=get_model(),
    tools=[great],
    input_guardrails=[check_input]

)

# result = Runner.run_sync(agent , "what is the capital of France ?")
# print(result.final_output)

async def main():
    result = await Runner.run(agent , "what is the capital of France ?")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())