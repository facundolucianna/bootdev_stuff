import os
from dotenv import load_dotenv
from google import genai
from google.genai import types # Importar types para facilitar el tipado
import argparse
from prompts import system_prompt
from call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print(api_key)
if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

config = types.GenerateContentConfig(
    tools=[available_functions], 
    system_instruction=system_prompt
)

def main():
    args = parser.parse_args()

    try: 
        # Mensaje inicial del usuario
        messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]

        # Bucle de turnos (User -> Model (Call) -> Tool (Result) -> Model (Answer))
        for _ in range(20):
            # CUIDADO: Verifica el nombre del modelo. 2.5 no existe, uso 2.0-flash-exp o 1.5-flash
            response = client.models.generate_content(
                model="gemini-2.5-flash", 
                contents=messages,
                config=config
            )

            if args.verbose:
                print(f"--- Turn Start ---")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            # 1. Agregamos la respuesta del modelo al historial INMEDIATAMENTE
            # (Sea texto o sea una llamada a función, el modelo necesita "recordar" que lo dijo)
            candidate = response.candidates[0]
            messages.append(candidate.content)

            # 2. Verificar si hay llamadas a función
            function_calls = response.function_calls # Helper del SDK nuevo
            
            if function_calls:
                function_call_responses_parts = []
                
                for function_call in function_calls:
                    if args.verbose:
                        print(f"Calling function: {function_call.name}")

                    # Ejecutar la función
                    function_call_result = call_function(function_call, verbose=args.verbose)

                    # Validaciones básicas (ajustar según lo que devuelva tu call_function)
                    if not function_call_result or not function_call_result.parts:
                         raise RuntimeError(f"Function {function_call.name} returned empty result")

                    # Asumimos que call_function devuelve una estructura compatible con Parts
                    part_response = function_call_result.parts[0]
                    function_call_responses_parts.append(part_response)

                    if args.verbose:
                        # Acceso seguro para imprimir (evita crash si no hay respuesta texto)
                        resp_text = part_response.function_response.response if part_response.function_response else "No text"
                        print(f"-> Result: {resp_text}")

                # 3. IMPORTANTE: Enviar la respuesta con role="tool"
                messages.append(types.Content(
                    role="tool", 
                    parts=function_call_responses_parts
                ))
                
                # El loop continúa para enviarle estos resultados al modelo
            
            else:
                # Si no hubo llamadas a función, es una respuesta de texto final
                if response.text:
                    print(response.text)
                break
                
    except Exception as e:
        print(f"Error: {e}")
        # Tip: Imprime el traceback completo para depurar mejor
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()