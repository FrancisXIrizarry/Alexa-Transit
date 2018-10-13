# HACK COOPER ALEXA SKILLS 
# USING SKILLBUILDER AND GOOGLE MAPS API


import logging
import requests
import googlemaps
import json

from datetime import datetime

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


    def find_key(strInput, search):
        list_string = strInput.split()
        loc = list_string[list_string.index(search) + 1]

        return loc

    def handle(self, handler_input):

        speech = "You can ask for directions"

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard("Starting...", speech)).set_should_end_session(
            False)
        return handler_input.response_builder.response

class MapIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("mapCall")(handler_input)

    def handle(self, handler_input):

        attributes = handler_input.request_envelope.request.intent.slots


        # logger.info(type(attributes))
        # logger.info(attributes.values())
        # start = attributes["fromLocation"]
        # finish = attributes["toLocation"]
        start = attributes.get('toLocation').to_dict()['value']
        finish = attributes.get('fromLocation').to_dict()['value']

        # logger.info(type(start))

        if " " in start:
            start.replace(" ", "+")
        if " " in finish:
            finish.replace(" ", "+")

        now = datetime.now()
        gmaps = googlemaps.Client(key='AIzaSyA1_wX9RiSvGhsrM8_JwFtcCeQ3b5LQfXM')
        path = gmaps.directions(start, finish, mode = "transit", departure_time = now)

        time = path[0]["legs"][0]["duration"]["text"]

        travel_mode = "Running"

        speech = "It will take " + time + " to reach "  + finish + " from "  + start + " by Train"

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard("Traveling", speech)).set_should_end_session(
            True)
        return handler_input.response_builder.response

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        
        speech = "Where would you like to go? Please tell me a start and ending location"

        handler_input.response_builder.speak(speech).ask(
            speech).set_card(SimpleCard(
                "Traveling", speech))
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        
        speech = "No worries, let me know when you need help!"

        handler_input.response_builder.speak(speech).set_card(
            SimpleCard("Traveling", speech))
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        
        speech = (
            "Unable to work with this information  "
            "You can ask me with a start and end point")
        reprompt = "You can say locations!!"
        handler_input.response_builder.speak(speech).ask(reprompt)
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
sb.add_request_handler(MapIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

handler = sb.lambda_handler()
