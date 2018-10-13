import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

def lambda_handler():
    # TODO implement
    print("Hello")

    handler_input.response_builder.speak("Hello from Cooper")

    return handler_input.response_builder

sb.add_request_handler(lambda_handler())

handler = sb.lambda_handler()