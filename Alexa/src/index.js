'use strict';

// --------------- Global Config -------------------------------------------------
const QUIZLETCLIENTID = process.env.QUIZLETCLIENTID;
const QUIZLETUSERNAME = process.env.QUIZLETUSERNAME;
const QUIZLETBASEURL = 'https://api.quizlet.com/2.0';

const request = require('request');



// --------------- Helpers that build all of the responses -----------------------

function buildSpeechletResponse(title, output, repromptText, shouldEndSession) {
    return {
        outputSpeech: {
            type: 'PlainText',
            text: output,
        },
        card: {
            type: 'Simple',
            title: `SessionSpeechlet - ${title}`,
            content: `SessionSpeechlet - ${output}`,
        },
        reprompt: {
            outputSpeech: {
                type: 'PlainText',
                text: repromptText,
            },
        },
        shouldEndSession,
    };
}

function buildResponse(sessionAttributes, speechletResponse) {
    return {
        version: '1.0',
        sessionAttributes,
        response: speechletResponse,
    };
}


/**
 * Fisher-Yates shuffle a dictionary
 * @param {Dict} terms - terms to be randomized 
 */
function randomizeTerms(terms) {
    var termsList = [];
    var newTerms = {};
    // Convert dict to list
    for (var t in terms) {
        termsList.push([t, terms[t]]);
    }
    // Randomize
    for (var i = termsList.length - 1; i > 0; i--) {
        var randidx = Math.floor(Math.random() * (i + 1));
        // Swap ith and random selected
        let temp = termsList[randidx].slice();
        termsList[randidx] = termsList[i].slice();
        termsList[i] = temp;
    }
    // Convert back to dict
    for (var i in termsList) {
        newTerms[termsList[i][0]] = termsList[i][1];
    }

    return newTerms;
}

// --------------- Functions that control the skill's behavior -----------------------

/**
 * Get the welcome message when skill started without intents
 * @param {Function} callback - Callback function that controls return value of lambda
 */
function getWelcomeResponse(callback) {
    // If we wanted to initialize the session to have some attributes we could add those here.
    const sessionAttributes = {};
    const cardTitle = 'Welcome';
    const speechOutput = 'Welcome to Quiz It! I\'m here to help you study. Using your uploaded text I have created a challenging problem set for you!' +
        'Say get quizes to start!';
    const repromptText = 'Start studying by saying get quizes'; // If user fails to answers or answer is unrecognized
    const shouldEndSession = false;

    callback(sessionAttributes,
        buildSpeechletResponse(cardTitle, speechOutput, repromptText, shouldEndSession));
}

/**
 * Get the quizes under the user account
 * @param {Dict} intent - Incoming intent, with parameters
 * @param {Dict} session - Session object holding session values
 * @param {Function} callback - Callback function that controls return value of lambda
 */
function retrieveQuizesAndStore(intent, session, callback) {
    var url = QUIZLETBASEURL + '/users/' + QUIZLETUSERNAME + '?client_id=' + QUIZLETCLIENTID;
    var sessionAttributes = {};
    var shouldEndSession = false;

    request(url, function(error, response, body) {

        if (error) throw error;

        var bodyObj = JSON.parse(body.toString());
        var sets = bodyObj.sets;
        var setTitles = [];
        var setIDs = [];

        for (var set in sets) {
            setTitles.push(sets[set].title);
            setIDs.push(sets[set].id)
        }

        sessionAttributes['setTitles'] = setTitles;
        sessionAttributes['setIDs'] = setIDs;

        var responseText = 'You have currently ' + sets.length + 
            (sets.length == 1 ? ' quiz ' : ' quizes ') + 
            'You can pick ';

        for (var i in setTitles) {
            if (setTitles.length > 1 && i == setTitles.length - 1) {
                responseText += 'or ';
            }
            responseText += setTitles[i] + ' ';
        }

        callback(sessionAttributes, buildSpeechletResponse(null, responseText, null, shouldEndSession));
    });
    return;
}


/**
 * Get the terms under the selectedd quiz
 * @param {Dict} intent - Incoming intent, with parameters
 * @param {Dict} session - Session object holding session values
 * @param {Function} callback - Callback function that controls return value of lambda
 */
function selectQuizAndGetTerms(intent, session, callback) {
    var setTitles = null;
    var setIDs = null; 

    if (session.attributes) {
        setTitles = session.attributes.setTitles;
        setIDs = session.attributes.setIDs;
    }

    var selectedQuiz = intent.slots.Quiz.value;
    var sessionAttributes = {};
    var responseText = null;
    var repromptText = null;
    var shouldEndSession = false;

    if (setTitles == null || setIDs == null) {
        // There has been an error. Quizes have not been retrieved
        responseText = 'Seems like you don\'t have any quizes.';
        repromptText = 'Try saying get quizes to retrive your quizes';
        callback(sessionAttributes, buildSpeechletResponse(null, responseText, repromptText, shouldEndSession));
        return;
    }

    // Copy attributes over
    for (var key in session.attributes) {
        sessionAttributes[key] = session.attributes[key];
    }

    // Search for requested quiz
    var selectedQuizID = null;
    for (var nameidx in setTitles) {
        if (setTitles[nameidx].toLowerCase() == selectedQuiz.toLowerCase()) {
            selectedQuizID = setIDs[nameidx];
        }
    }
    if (!selectedQuizID) {
        // Selected a quiz that doesn't exist
        responseText = 'Oops that\'s not one of your quizes. Try picking another quiz!';
        repromptText = 'Try picking another quiz!';
        callback(sessionAttributes, buildSpeechletResponse(null, responseText, repromptText, shouldEndSession));
        return;
    }

    // Query id good
    sessionAttributes['selectedQuiz'] = selectedQuiz; // Store selected quiz
    var url = QUIZLETBASEURL + '/sets/' + selectedQuizID + '?client_id=' + QUIZLETCLIENTID;
    request(url, function(error, response, body) {
        if (error) throw error;
        
        var bodyObj = JSON.parse(body.toString());
        var terms = bodyObj.terms;
        var termItems = {};
        for (var term in terms) {
            termItems[terms[term].term] = terms[term].definition;
        }
        termItems = randomizeTerms(termItems);

        sessionAttributes['terms'] = termItems; // Store new terms
        sessionAttributes['currentTerm'] = 0; // Store index of current question

        responseText = 'Let\'s start! First question. ';
        responseText += Object.keys(termItems)[0];
        repromptText = Object.keys(termItems)[0];

        callback(sessionAttributes, buildSpeechletResponse(repromptText, responseText, repromptText, shouldEndSession));
        return;
    });
}


function answerQuestionAndCheck(intent, session, callback) {
    var responseText = null;
    var repromptText = null;
    var shouldEndSession = false;
    var sessionAttributes = {}
    var answer = null;
    var questionAnswerPair = {};
    var terms = {};
    

    // Copy attributes over
    for (var key in session.attributes) {
        sessionAttributes[key] = session.attributes[key];
    }

    var currentQuestionKey = null;
    var currentQuestionTerm = null;
    
    if (session.attributes.terms != null && session.attributes.currentTerm != null) {
        terms = session.attributes.terms;
        currentQuestionKey = Object.keys(terms)[session.attributes.currentTerm]
        questionAnswerPair[currentQuestionKey] = session.attributes.terms[currentQuestionKey];
    }

    // Get the answer
    answer = intent.slots.Answer.value;

    var retry = false;
    if (terms == null || currentQuestionKey == null || questionAnswerPair == null || answer == null) {
        // Something went wrong with the request. Re-ask the same question
        responseText = 'Oh something went wrong, let\'s try that again. ';
        retry = true;
    } else if (answer.toLowerCase() != questionAnswerPair[currentQuestionKey].toLowerCase()) {
         // Wrong answer
        responseText = 'Hmm that doesn\'t seem right. let\'s try that again. ';
        retry = true;
    }
    if (retry) {
        responseText += currentQuestionKey;
        repromptText = currentQuestionKey;
        callback(sessionAttributes, buildSpeechletResponse('Try Again!', responseText, repromptText, shouldEndSession));
        return;
    }

    // Answer is correct
    responseText = 'Correct! ';
    var lastQuestion = false;
    if (session.attributes.currentTerm == Object.keys(terms).length - 1) {
        // That was the last question
        responseText += 'Congratulations! You have bested me. Say get quiz to start again.';
        repromptText = 'Say get quiz to start again.';
        callback({}, buildSpeechletResponse('Congratulations!', responseText,  repromptText, shouldEndSession));
        return;
    } else if (session.attributes.currentTerm == Object.keys(terms).length - 2) {
        // If it was the second last question
        responseText += 'Last question! ';
        lastQuestion = true;
    }
    sessionAttributes['currentTerm'] = session.attributes.currentTerm + 1; // Next question
    responseText += (!lastQuestion ? 'Next question! ' : '') + Object.keys(terms)[sessionAttributes['currentTerm']];
    repromptText = Object.keys(terms)[sessionAttributes['currentTerm']];

    callback(sessionAttributes, buildSpeechletResponse('Next question!', responseText, repromptText, shouldEndSession));
    return;
}


/**
 * Handle session end call
 * @param {Function} callback - Callback func to return value of lambda
 */
function handleSessionEndRequest(callback) {
    const cardTitle = 'Session Ended';
    const speechOutput = 'Thank you for trying the Alexa Skills Kit sample. Have a nice day!';
    // Setting this to true ends the session and exits the skill.
    const shouldEndSession = true;

    callback({}, buildSpeechletResponse(cardTitle, speechOutput, null, shouldEndSession));
}


// --------------- Events -----------------------

/**
 * Called when the session starts.
 */
function onSessionStarted(sessionStartedRequest, session) {
    console.log(`onSessionStarted requestId=${sessionStartedRequest.requestId}, sessionId=${session.sessionId}`);
}

/**
 * Called when the user launches the skill without specifying what they want.
 */
function onLaunch(launchRequest, session, callback) {
    console.log(`onLaunch requestId=${launchRequest.requestId}, sessionId=${session.sessionId}`);

    // Dispatch launch.
    getWelcomeResponse(callback);
}

/**
 * Called when the user specifies an intent for this skill.
 */
function onIntent(intentRequest, session, callback) {
    console.log(`onIntent requestId=${intentRequest.requestId}, sessionId=${session.sessionId}`);

    const intent = intentRequest.intent;
    const intentName = intentRequest.intent.name;

    // Dispatch to your skill's intent handlers
    if (intentName === 'GetQuizes') {
        retrieveQuizesAndStore(intent, session, callback);
    } else if (intentName === 'QuizMe') {
        selectQuizAndGetTerms(intent, session, callback);
    } else if (intentName === 'AnswerQuestion') {
        answerQuestionAndCheck(intent, session, callback);
    } else if (intentName === 'AMAZON.HelpIntent') {
        getWelcomeResponse(callback);
    } else if (intentName === 'AMAZON.StopIntent' || intentName === 'AMAZON.CancelIntent') {
        handleSessionEndRequest(callback);
    } else {
        throw new Error('Invalid intent');
    }
}

/**
 * Called when the user ends the session.
 * Is not called when the skill returns shouldEndSession=true.
 */
function onSessionEnded(sessionEndedRequest, session) {
    console.log(`onSessionEnded requestId=${sessionEndedRequest.requestId}, sessionId=${session.sessionId}`);
    // Add cleanup logic here
}


// --------------- Main handler -----------------------

// Route the incoming request based on type (LaunchRequest, IntentRequest,
// etc.) The JSON body of the request is provided in the event parameter.
exports.handler = (event, context, callback) => {
    try {
        console.log(`event.session.application.applicationId=${event.session.application.applicationId}`);

        // Check valid app ID        
        if (event.session.application.applicationId !== 'amzn1.ask.skill.6aa36c75-a8d3-4985-97ba-ad7cb57711b0') {
             callback('Invalid Application ID');
        }

        if (event.session.new) {
            onSessionStarted({ requestId: event.request.requestId }, event.session);
        }

        if (event.request.type === 'LaunchRequest') {
            onLaunch(event.request,
                event.session,
                (sessionAttributes, speechletResponse) => {
                    callback(null, buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === 'IntentRequest') {
            onIntent(event.request,
                event.session,
                (sessionAttributes, speechletResponse) => {
                    callback(null, buildResponse(sessionAttributes, speechletResponse));
                });
        } else if (event.request.type === 'SessionEndedRequest') {
            onSessionEnded(event.request, event.session);
            callback();
        }
    } catch (err) {
        callback(err);
    }
};
