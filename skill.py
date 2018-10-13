# HACK COOPER ALEXA SKILLS 
# USING SKILLBUILDER AND GOOGLE MAPS API


import logging
import requests

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        start = handler_input["destination_addresses"]
        finish = handler_input["origin_addresses"]

        payload = {"origins" : start, "destinations" : finish, "key" : "AIzaSyA1_wX9RiSvGhsrM8_JwFtcCeQ3b5LQfXM"}

        req = requests.post("https://maps.googleapis.com/maps/api/distancematrix/json", params = payload )
        res = req.json()
        time = handler_input["rows"]["elements"]["duration"]["text"]
        travel_mode = "Running"
        speech = "It will take " + time + "to reach " + finish + "from " + start + "using " + travel_mode

        speech_text = "Welcome to the Alexa Skills Kit, you can say hello!"

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard("Traveling from " + start + "to " + finish, speech)).set_should_end_session(
            False)
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        
        speech_text = "Where would you like to go? Please tell me a start and ending location"

        handler_input.response_builder.speak(speech_text).ask(
            speech_text).set_card(SimpleCard(
                "Where would you like to go?", speech_text))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        
        speech_text = "No worries, let me know when you need help!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Cancelling", speech_text))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        
        speech_text = (
            "Unable to work with this information  "
            "You can ask me with a start and end point")
        reprompt = "You can say hello!!"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    
    def can_handle(self, handler_input):
        
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        
        return handler_input.response_builder.response

class CatchAllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        
        return True

    def handle(self, handler_input, exception):
        
        logger.error(exception, exc_info=True)

        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)

        return handler_input.response_builder.response



sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()