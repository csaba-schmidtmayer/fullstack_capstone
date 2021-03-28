#!/bin/bash
export FLASK_APP=app
export FLASK_ENV=development

export AUTH0_DOMAIN=schmiczy.eu.auth0.com
export ALGORITHMS=RS256
export API_AUDIENCE=https://api.casting-agency.schmiczy.eu

flask run