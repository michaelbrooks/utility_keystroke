######################

# coding: utf8
MAX_TYPOS = 1
MIN_STDEV = 6
KEYPHRASE = "The quick brown fox jumps over the lazy dog"
REQUIRED_RECORDINGS = 6
FAIL_CHANCE = 0.00
NUM_ASSOCIATIONS = 3
ENROLL_PRICE = 0.04

import random, hashlib, uuid, datetime, time, math
import gluon.contrib.simplejson

messages = dict(
    terse = dict(
        recordSuccess = "Example recorded.",
        recordAllDone = "Recorded all examples.",
        verifySuccess = "Verified.",
        verifyError = "Not recognized. Retry.",
        validateNotTyped = "Error. Retry.",
        validateTypos = "Bad typing sample. Retry.",
        validateStats = "Error. Retry."
    ),
    medium = dict(
        recordSuccess = "Typing pattern recorded.",
        recordAllDone = "Recorded all required examples.",
        verifySuccess = "Keystroke pattern verified.",
        verifyError = "Keystroke pattern not recognized. Try again.",
        validateNotTyped = "Error detecting keystrokes. Try again.",
        validateTypos = "Too many typos. Try again.",
        validateStats = "Error detecting keystrokes. Try again."
    ),
    verbose = dict(
        recordSuccess = "You successfully recorded your typing patterns.",
        recordAllDone = "You have recorded all of the needed examples of your typing patterns.",
        verifySuccess = "Your keystroke pattern was verified!",
        verifyError = "Sorry, your keystroke pattern was not recognized. Please try again.",
        validateNotTyped = "Sorry, there was a problem detecting your typing patterns. Please type the phrase normally.",
        validateTypos = "Sorry, there were too many typos. Please try to type the phrase more carefully.",
        validateStats = "Sorry, there was a problem detecting your typing patterns. Please type the phrase normally."
    ),
    authInstructions = "Type the following phrase normally.",
    recordInstructions = "keystroke", # Options: keystroke
    verifyInstructions = "keystroke", # Options: keystroke
)

def set_message(message, type):
    print message, type
    if message is not None:
        response.flash = message
        response.flashType = type

def get_message(msgName):
    if request.message_length == 'none':
        return " "

    msg = messages[request.message_length][msgName]
    if request.message_size == 'large':
        msg = msg.upper()
    return msg

if session.flashType:
    response.flashType = session.flashType
    session.flashType = None

response.session = session
response.title = "Mood Study"

verificationAnswers = [
    "cow",
    "horse",
    "pig",
    "chicken",
    "lizard",
    "duck",
    "sheep",
    "dog",
    "cat",
    "fish",
    "penguin",
    "elephant",
    "giraffe"
]

verifications = [
    {"code":"fGRBdfmsoE", "answer":"chicken"},
    {"code":"pzXuFeat2D", "answer":"cat"},
    {"code":"jY03hZbM3G", "answer":"elephant"},
    {"code":"Sx9oL4sXMJ", "answer":"sheep"},
    {"code":"lXvWqk1b1o", "answer":"cow"},
    {"code":"IhX17rARJ9", "answer":"chicken"},
    {"code":"Z4tlHSvndP", "answer":"lizard"},
    {"code":"rC5vPxC1JV", "answer":"horse"},
    {"code":"DCwGF1DPYR", "answer":"dog"},
    {"code":"RlpOflCqUS", "answer":"horse"},
    {"code":"6qN7XLChXd", "answer":"penguin"},
    {"code":"1PJjDX5NUp", "answer":"pig"},
    {"code":"ybogV7ohqG", "answer":"dog"},
    {"code":"noZzU4M7uT", "answer":"cow"},
    {"code":"FLGFG9OEGf", "answer":"lizard"},
    {"code":"mx4qXwPtaJ", "answer":"giraffe"},
    {"code":"fBuQfGgxxh", "answer":"fish"},
    {"code":"0iBVgqT2oN", "answer":"horse"},
    {"code":"fp8WRPMCWJ", "answer":"elephant"},
    {"code":"hgendcJot7", "answer":"horse"},
    {"code":"t3xJEqangh", "answer":"giraffe"},
    {"code":"aR0SWYyl4H", "answer":"dog"},
    {"code":"lqyCGoW7nX", "answer":"cat"},
    {"code":"37zVw4yY8G", "answer":"sheep"},
    {"code":"MEzPbkeQII", "answer":"giraffe"},
    {"code":"YNO37YE9zP", "answer":"penguin"},
    {"code":"xJRF9wBviB", "answer":"duck"},
    {"code":"9T66hl3ruv", "answer":"penguin"},
    {"code":"iCHgq2CLSs", "answer":"sheep"},
    {"code":"D35tgq0FLn", "answer":"cat"},
    {"code":"sCxwDCQuHn", "answer":"elephant"},
    {"code":"ILNGtlB4FN", "answer":"fish"},
    {"code":"PxtPh7iK9v", "answer":"lizard"},
    {"code":"b9ypnd0Txb", "answer":"duck"},
    {"code":"VtFRAICFGF", "answer":"lizard"},
    {"code":"g3fSmKn6yY", "answer":"sheep"},
    {"code":"yRneW8CTqY", "answer":"cat"},
    {"code":"YrQFB2oVHW", "answer":"fish"},
    {"code":"wHSEGWMwAt", "answer":"pig"},
    {"code":"pnzXySwQKK", "answer":"elephant"},
    {"code":"aMhaFAhlXu", "answer":"pig"},
    {"code":"Pfrzr0jrTo", "answer":"duck"},
    {"code":"DbVzqBni7i", "answer":"dog"},
    {"code":"VXCPHcXvp7", "answer":"penguin"},
    {"code":"DCCuIUaED2", "answer":"chicken"},
    {"code":"IUacrJDHTs", "answer":"cow"},
    {"code":"7Phtq9fBNW", "answer":"giraffe"},
    {"code":"WBgX6RCem7", "answer":"chicken"},
    {"code":"spUVHcVJBh", "answer":"cow"},
    {"code":"RrQsTKsrq8", "answer":"duck"},
    {"code":"xufN9TJeMi", "answer":"pig"},
    {"code":"IardZqBAGk", "answer":"fish"}
]

association_list = [
    "afraid",
    "blue",
    "citizen",
    "decorum",
    "fall",
    "hammer",
    "justice",
    "month",
    "pretty",
    "satisfied",
    "smooth",
    "swift",
    "wash",
    "anger",
    "book",
    "city",
    "deep",
    "family",
    "hand",
    "king",
    "moon",
    "priest",
    "scissors",
    "soft",
    "swim",
    "water",
    "anxiety",
    "box",
    "close",
    "despise",
    "fiance(e)",
    "happiness",
    "kiss",
    "moral",
    "proud",
    "scold",
    "soldier",
    "sympathy",
    "whiskey",
    "attend",
    "boy",
    "cold",
    "die",
    "finger",
    "hard",
    "lamp",
    "mountain",
    "prune",
    "scorn",
    "sour",
    "table",
    "whistle",
    "baby",
    "bread",
    "comfort",
    "dispute",
    "flowers",
    "hay",
    "lie",
    "music",
    "pure",
    "sea",
    "spider",
    "thief",
    "white",
    "bath",
    "brother",
    "command",
    "divorce",
    "foot",
    "head",
    "light",
    "mutton",
    "question",
    "sheep",
    "square",
    "thirsty",
    "wild",
    "beautiful",
    "butter",
    "cook",
    "doctor",
    "foreign",
    "health",
    "lion",
    "needle",
    "quiet",
    "ship",
    "stem",
    "to fear",
    "window",
    "bed",
    "butterfly",
    "cottage",
    "door",
    "friendly",
    "heavy",
    "long",
    "new",
    "red",
    "short",
    "stick",
    "tobacco",
    "wish",
    "bible",
    "cabbage",
    "count",
    "dream",
    "frog",
    "high",
    "loud",
    "ocean",
    "religion",
    "sick",
    "stomach",
    "tree",
    "woman",
    "big",
    "carpet",
    "cow",
    "eagle",
    "fruit",
    "hit",
    "magazine",
    "old",
    "rich",
    "sickness",
    "stork",
    "trip",
    "working",
    "bird",
    "chair",
    "dance",
    "earth",
    "fur",
    "house",
    "man",
    "paint",
    "river",
    "sin",
    "stove",
    "trouble",
    "wrong",
    "bitter",
    "cheese",
    "dark",
    "eating",
    "girl",
    "hunger",
    "marry",
    "part",
    "rough",
    "sing",
    "street",
    "turnip",
    "yellow",
    "black",
    "child",
    "dear",
    "evil",
    "glass",
    "ink",
    "memory",
    "pencil",
    "sad",
    "sleep",
    "stupid",
    "unjust",
    "blossom",
    "choose",
    "death",
    "expensive",
    "green",
    "joy",
    "money",
    "pray",
    "salt",
    "slow",
    "sweet",
    "village"
]

moodTerms = [
    ('happy', 'm_happy'),
    ('sad', 'm_sad'),
    ('lively', 'm_lively'),
    ('drowsy', 'm_drowsy')
]

hit_session = None

def index():

    if request.preview:
        return welcome(None)
    
    # Make sure this is the only HIT that the user is progressing through
    if not block_multiple(None):
        # We're blocked, so show the welcome screen in the background
        response.view = 'keystroke/index.html'
        return welcome(None)
    
    # At this point we assume that the user is really doing this HIT
    # In other words, hit_session is set up correctly
    if 'next_step' not in hit_session:
        
        hit_count = hits_done(request.workerid, request.study)
    
        # Check the GET variables for debugging
        if not request.live and ("hits_completed" in request.vars):
            hit_count = int(request.vars.hits_completed)
        
        if hit_count == 0:
            # No next step set and no hits done, we show the welcome message
            hit_session.next_step = 'welcome'
            response.view = 'keystroke/index.html'
            return welcome(None)
        else:
            # No next step set and at least 1 hit done, we go to verification
            hit_session.next_step = 'verify'
            response.view = 'keystroke/verify.html'
            return verify(None)
            
    if hit_session.next_step == 'welcome':
        # Show the welcome screen
        response.view = 'keystroke/index.html'
        return welcome(None)
    if hit_session.next_step == 'thanks':
        # We're done. This should probably not happen on MTurk.
        response.view = 'keystroke/thanks.html'
        return thanks(None)
    if hit_session.next_step == 'enroll':
        # We're doing enrollment next
        response.view = 'keystroke/record.html'
        return enroll(None)
    if hit_session.next_step == 'register':
        # We've done enrollment and going on to post-enrollment questions
        response.view = 'keystroke/register.html'
        return register(None)
    if hit_session.next_step == 'verify':
        # We're going to attempt authentication
        response.view = 'keystroke/verify.html'
        return verify(None)
    if hit_session.next_step == 'mood_test':
        # We've authenticated, so now we are going to do the task
        response.view = 'keystroke/mood_test.html'
        return mood_test(None)
    if hit_session.next_step == 'free_write':
        # We've done the mood test, now time for the free writing
        response.view = 'keystroke/free_write.html'
        return free_write(None)
    if hit_session.next_step == 'association':
        # We've done the free writing, time for the word association
        response.view = 'keystroke/association.html'
        return association(None)

# Display a welcome message or continue on to enrollment
def welcome(param):
    
    if request.preview:
        # don't bother to do much on preview, just show the screen
        return dict(messages=messages)
    
    # If the user has clicked the "Get Started" button, then
    # the GET variable "enroll" will be set.
    if request.vars.enroll:
        hit_session.next_step = 'register'
        
        # remove the enroll parameter
        del request.get_vars['enroll']
        
        # Go home and try again
        redirect(URL(f='index', vars=request.get_vars))
    
    response.isEnrollment = True
    request.enrollPrice = ENROLL_PRICE
    request.verifyPrice = request.price;
    
    return dict(messages=messages)

# Display the recording screen for enrollment
# until enough recordings are collected, then go on to the survey.
def enroll(param):
    
    #Initialize successfulRecordings to 0 if not set yet
    if 'successfulRecordings' not in hit_session:
        hit_session.successfulRecordings = 0

    # set up the auth form
    form = auth_form(messages['authInstructions'], KEYPHRASE)
    
    #validate the recording if it is set
    if form.process(onsuccess=None, onfailure=None).accepted and validate(request.vars.typing, request.vars.text, form):
        record_action('user recorded', request.vars.typing)
        set_message(get_message('recordSuccess'), 'success')
        hit_session.successfulRecordings += 1
    elif form.errors:
        record_action('invalid: record', form.errors)
        
    #They've submitted all required recordings
    if hit_session.successfulRecordings >= REQUIRED_RECORDINGS:
        record_action('recordings completed')
        
        # complete the HIT
        del session[session.current_hit]
        session.current_hit = None
        
        # set the price to the enrollment price
        alter_price(ENROLL_PRICE)
        hit_finished()
        
        # Prepare to give thanks
        session.flash = "The HIT has been submitted."
        session.flashType = "success"
        hit_session.next_step = 'thanks'
        
        # Go home and try again, but probably MTurk will takeover now
        redirect(URL(f='index', vars=request.get_vars))
        
    response.isEnrollment = True
    request.enrollPrice = ENROLL_PRICE
    request.verifyPrice = request.price;
    
    # If they've submitted some recordings successfully already, scroll down
    if hit_session.successfulRecordings > 0:
        request.scrollDown = True
    
    result = dict()
    result['keyphrase'] = KEYPHRASE
    result['requiredRecordings'] = REQUIRED_RECORDINGS
    result['successfulRecordings'] = hit_session.successfulRecordings
    result['form'] = form
    result['messages'] = messages
    return result

# Show a post-enrollment questionnaire
# Mark the HIT done when submitted.
def register(param):
    
    # Set this to 0 if not yet set
    if 'invalid_verifs' not in hit_session:
        hit_session.invalid_verifs = 0
    
    form = get_register_form(param)
    
    if form.process(onfailure="").accepted:
    
        # save the form answers
        record_entry_survey(request.post_vars)
        
        # Reset the verification failure counter
        hit_session.invalid_verifs = 0
        
        hit_session.next_step = 'enroll'
        
        # Go home and try again
        redirect(URL(f='index', vars=request.get_vars))
        
    elif form.errors:
        if 'verify' in form.errors:
            # there was a verification error
            hit_session.invalid_verifs += 1
        
        record_action('invalid: register', form.errors)
        
    response.isEnrollment = True
    request.enrollPrice = ENROLL_PRICE
    request.verifyPrice = request.price;
    
    return dict(form=form, messages=messages)

# Show the authentication form
# Advance to surveys if successful
def verify(param): 

    # Initialize the attempt counter
    if 'attempts' not in hit_session:
        hit_session.attempts = 0

    form = auth_form(messages['authInstructions'], KEYPHRASE)
    
    if form.process(onsuccess=None, onfailure=None).accepted and validate(request.vars.typing, request.vars.text, form):
        #validate the recording (the user XYZ is a dummy user here)
        if authorize("XYZ"):
            #if they were authenticated, go on to questionnaire
            record_action('user authorized', request.vars.typing)
            hit_session.next_step = 'mood_test'
            set_message(get_message('verifySuccess'), 'success')
            # Go home and try again
            redirect(URL(f='index', vars=request.get_vars))
        else:
            # Not authorized so show a denied error
            record_action('user denied', request.vars.typing)
            set_message(get_message('verifyError'), 'error')
            #form.errors = dict(text=get_message('verifyError'))
            
    elif form.errors:
        # Invalid verification attempt
        record_action('invalid: verify', form.errors)

    # Increase the count of verification attempts
    hit_session.attempts += 1
        
    return dict(keyphrase=KEYPHRASE, form=form, messages=messages)

# Show the mood test and advance to word
# association when done.
def mood_test(param):

    form = get_mood_form(param);
    
    if form.process(onfailure="").accepted:
        # save the mood form for later
        hit_session.mood_form = request.post_vars
        
        hit_session.next_step = 'association'
        
        # Go home and try again
        redirect(URL(f='index', vars=request.get_vars))
        
    elif form.errors:
        record_action('invalid: verified', form.errors)
        
    return dict(form=form, messages=messages)

# Display a text area with instructions for free writing.
# When submitted, the HIT is done.
def free_write(param):

    form = get_free_write_form(param);
    
    if form.process(onfailure="").accepted:
        # save the free writing in the session
        hit_session.free_write_text = request.post_vars.text
        hit_session.free_write_time = request.post_vars.time
        
        # Save everything
        record_post_survey()
        
        # complete the HIT
        del session[session.current_hit]
        session.current_hit = None
        hit_finished()
        
        # Prepare to give thanks
        session.flash = "The HIT has been submitted."
        session.flashType = "success"
        hit_session.next_step = 'thanks'
        
        # Go home and try again
        redirect(URL(f='index', vars=request.get_vars))
        
    elif form.errors:
        record_action('invalid: verified', form.errors)
        
    return dict(form=form, messages=messages)

# Display a series of one-word prompts.
# When all have been collected, go to free writing.
def association(param):
    
    #Initialize associations to 0 if not set yet
    if 'associations' not in hit_session:
        hit_session.associations = {}
        hit_session.association_times = {}
    
    form, promptWordBox, hiddenPromptWord, submitButton = get_association_form(param);
    
    if form.process(onfailure="").accepted:
        # save this word association
        prompt_word = request.post_vars['prompt_word']
        
        hit_session.associations[prompt_word] = request.post_vars['response_word']
        hit_session.association_times[prompt_word] = request.post_vars['time']
        
        # We need to edit the form we're displaying since we just validated the submission
        prompt_word, button_label = get_prompt_word(None)
        hiddenPromptWord['_value'] = prompt_word
        promptWordBox[0] = prompt_word
        submitButton['_value'] = button_label
        
    elif form.errors:
        record_action('invalid: verified', form.errors)
    
    if len(hit_session.associations) >= NUM_ASSOCIATIONS:
        
        hit_session.next_step = 'free_write'
        
        # Go home and try again
        redirect(URL(f='index', vars=request.get_vars))
    
    return dict(form=form, messages=messages)

# Display a thank you message
def thanks(param):
    
    return dict(messages=messages)
    
##
## These are private functions
##

def initialize_hit(hitid):
    log_action('initialized hit')
    session.current_hit = hitid
    session[hitid] = gluon.storage.Storage()
    session.start_time = time.time()

# Checks if the user is already doing a different HIT
# If so, shows the warning screen
# If not, returns True
def block_multiple(parameter):
    global hit_session
    
    hit = request.hitid
    
    if not session.current_hit:
        # we are not doing a hit currently
        initialize_hit(hit)
        hit_session = session[session.current_hit]
        
        # We're good to go
        return True
        
    elif session.current_hit != hit:
        # they are starting a new hit while doing another hit
        if request.vars.unblock:
            # they've said they don't care, they want to do this one anyway
            record_action('unblocked')
            initialize_hit(hit)
            hit_session = session[session.current_hit]

            # Remove the unblock parameter
            del request.get_vars['unblock']
            
            # We're good to go, but have to redirect to remove the unblock parameter
            redirect(URL(f='index', vars=request.get_vars))
        else:
            # They haven't unblocked us, so we have to stay here
            record_action('blocked')
            response.block = True
            
            # We return False beause we're blocked
            return False
    else:
        # We're continuing an old HIT
        hit_session = session[session.current_hit]
        #And we're good to go
        return True

def get_mood_item(labelText, reverseLabelText, name):
    return DIV(
        DIV(_class="checkmark fade"),
        DIV(labelText, _class="positive mood-label"),
        DIV(_class="slider"),
        DIV(reverseLabelText, _class="negative mood-label"),
        INPUT(_name=name, _type="hidden"),
        _class="mood item clearfix", _id=name)
        
# Get the mood test questionnaire
def get_mood_form(param):
    
    form = FORM(
        DIV(
            "Adjust the sliders below to indicate how well each word describes your present mood:",
            BR(),
            #I("Note: you must adjust each slider."),
            _class="instructions"),
        _id="mood-form", _class="questions well clearfix")

    # form.append(DIV(
        # DIV("Definitely feel", _class="left"),
        # DIV("Not sure", _class="middle"),
        # DIV("Definitely do not feel", _class="right"),
        # _class="legend clearfix"))
    
    moodItems = moodTerms
    random.shuffle(moodItems)
    for name, key in moodItems:
        form.append(get_mood_item(name, 'not ' + name, key))
    
    form.append(P("Overall, my mood is:"))
    
    form.append(get_mood_item("Very Pleasant", "Very Unpleasant", "m_overall"))
    
    form.append(DIV(INPUT(_type="submit",_name='submit', _id='submit', _value="Next Page", _class="btn btn-primary btn-large"),
                    _class="form-footer"))
    
    return form

# Get the free writing form
def get_free_write_form(param):
    form = FORM(
        DIV(
            P("In the box below, please write a paragraph of about 3 lines in a stream-of-consciousness style."),
            UL(
                LI("Start with whatever your mind thinks of first. It doesn't matter what it is."),
                LI("Don't worry about grammar or structure."),
                LI("Allow your thoughts to drift freely."),
                LI("Don't edit what you've written.")
            ),
            _class="instructions"),
        INPUT(_name="time", _type="hidden"),
        TEXTAREA(_name="text", _id="free-write-box", requires=IS_NOT_EMPTY(error_message="You must submit some writing")),
        _id="free-write-form", _class="questions well clearfix")

        
    submit = submit_button('submit', True)
    submit.insert(0, DIV(_class="checkmark fade"))
    form.append(DIV(
        submit,
        _class="form-footer"
        ))
    
    return form

def get_prompt_word(param):
    hitNumber = hits_done(request.workerid, request.study)
    if not request.live and ("hits_completed" in request.vars):
        hitNumber = int(request.vars.hits_completed)
    
    promptIndex = NUM_ASSOCIATIONS * (hitNumber - 1) + len(hit_session.associations)
        
    prompt_word = association_list[promptIndex]
    
    buttonLabel = "Next Word"
    if len(hit_session.associations) == NUM_ASSOCIATIONS - 1:
        buttonLabel = "Next Page"

    return prompt_word, buttonLabel
    
def get_association_form(param):

    prompt_word, buttonLabel = get_prompt_word(param)
    hiddenPromptWord = INPUT(_name="prompt_word", _type="hidden", _value=prompt_word)
    promptWordBox = DIV(prompt_word, _class="prompt-word-box")
    submitButton = INPUT(_type="submit",_name='submit', _id='submit', _disabled="disabled", _value=buttonLabel, _class="btn btn-primary btn-large")
    
    form = FORM(
        DIV(P("Type as quickly as possible the first word that occurs to your mind."),
            I("Press the green button to begin."),
            _class="instructions"),
        INPUT(_name="time", _type="hidden"),
        hiddenPromptWord,
        DIV(BUTTON("I'm ready. Show the prompt word.", 
            _class="ready-button btn btn-success btn-large"),
            _class="prep-area"),
        DIV(
            promptWordBox,
            INPUT(_name="response_word", _type="text", _autocomplete="off", _class="response-word-box",
                requires=IS_NOT_EMPTY(error_message="You must respond with a word")),
            BR(),
            submitButton,
            _class="response-area fade"
        ),
        _id="association-form", _class="questions well clearfix"
    )
    
    return form, promptWordBox, hiddenPromptWord, submitButton
    
# Get the post enrollment questionnaire
def get_register_form(param):
    ageItem = form_item("What is your age, in years? (required)", 
        INPUT(_type="text",_name="age",_autocomplete="off", requires=[
            IS_NOT_EMPTY(error_message="Age is required"), 
            IS_INT_IN_RANGE(0, 200,error_message="Enter your age in years"),
            IS_INT_IN_RANGE(18, 200, error_message="You must be 18 or older to participate")]))
    
    occupationItem = form_item("What is your occupation? (required)", 
        INPUT(_type="text",_name="occupation",_autocomplete="off",
        requires=IS_NOT_EMPTY(error_message="Occupation is required")))
    
    genderInputs = [
        LABEL(INPUT(_type="radio", _name="gender", _value='female', _id="gender-female", requires=IS_NOT_EMPTY(error_message="Gender is required")),
            'Female',
            _for="gender-female", _class="radio"),
        LABEL(INPUT(_type="radio", _name="gender", _value='male', _id="gender-male"),
            'Male',
            _for="gender-male", _class="radio")
    ]
    genderItem = form_item("What is your gender? (required)", genderInputs)
  
    incomeInputs = [
        LABEL(INPUT(_type="radio", _name="income", _value='0', _id="income-0", requires=IS_NOT_EMPTY(error_message="Income is required")),
            'Less than $10,000',
            _for="income-0", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='1', _id="income-1"),
            '$10,000 to $19,999',
            _for="income-1", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='2', _id="income-2"),
            '$20,000 to $29,999',
            _for="income-2", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='3', _id="income-3"),
            '$30,000 to $39,999',
            _for="income-3", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='4', _id="income-4"),
            '$40,000 to $49,999',
            _for="income-4", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='5', _id="income-5"),
            '$50,000 to $59,999',
            _for="income-5", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='6', _id="income-6"),
            '$60,000 to $69,999',
            _for="income-6", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='7', _id="income-7"),
            '$70,000 to $79,999',
            _for="income-7", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='8', _id="income-8"),
            '$80,000 to $89,999',
            _for="income-8", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='9', _id="income-9"),
            '$90,000 to $99,999',
            _for="income-9", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='10', _id="income-10"),
            '$100,000 to $149,999',
            _for="income-10", _class="radio"),
        LABEL(INPUT(_type="radio", _name="income", _value='11', _id="income-11"),
            '$150,000 or more',
            _for="income-11", _class="radio"),
    ]
    incomeItem = form_item("What is your total annual household income in US dollars? (required)", incomeInputs)
    
    moodInputs = [
        LABEL(INPUT(_type="radio", _name="mood", _value='0', _id="mood-no", requires=IS_NOT_EMPTY(error_message="You must answer the question about mood history.")),
            'No',
            _for="mood-no", _class="radio"),
        LABEL(INPUT(_type="radio", _name="mood", _value='1', _id="mood-yes"),
            'Yes',
            _for="mood-yes", _class="radio"),
        LABEL(INPUT(_type="radio", _name="mood", _value='2', _id="mood-null"),
            'Decline to answer',
            _for="mood-null", _class="radio"),
    ]
    moodItem = form_item("Have you every been diagnosed with a mood disorder or been prescribed mood stabilizing medication? (required)", moodInputs)
    
    biometricInputs = [
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='fingerprint', _id="biometric-fingerprint", requires=IS_NOT_EMPTY(error_message="You must answer the question about identification systems.")),
            'Fingerprints',
            _for="biometric-fingerprint", _class="checkbox"),
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='eye', _id="biometric-eye"),
            'Iris or retina scans',
            _for="biometric-eye", _class="checkbox"),
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='face', _id="biometric-face"),
            'Face recognition',
            _for="biometric-face", _class="checkbox"),
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='voice', _id="biometric-voice"),
            'Voice recognition',
            _for="biometric-voice", _class="checkbox"),
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='signature', _id="biometric-signature"),
            'Signature recognition',
            _for="biometric-signature", _class="checkbox"),
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='keystroke', _id="biometric-keystroke"),
            'Keystroke (typing) pattern',
            _for="biometric-keystroke", _class="checkbox"),
    ]
    biometricInputs = randomize('biometric', biometricInputs);
    biometricInputs.append(
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='other', _id="biometric-other"),
            'Other biometric systems',
            _for="biometric-other", _class="checkbox"))
    biometricInputs.append(
        LABEL(INPUT(_type="checkbox", _name="biometric", _value='none', _id="biometric-none"),
            'I have never used any of these',
            _for="biometric-none", _class="checkbox"))
    
    set_exclusion('biometric', 'biometric-none')
    
    biometricItem = form_item("Which of the following identification or authentication systems have you used before? (required)", biometricInputs)
    
    verificationItem = verify_item('verify')
    
    submitButton = INPUT(_type="submit",_name='submit', _id='submit', _value='Next Page', _class="btn btn-primary btn-large")
    
    form = FORM(ageItem, genderItem, occupationItem, incomeItem, moodItem, biometricItem, verificationItem, submitButton, _id="register-form", _class="questions well clearfix")
    
    return form
            
def submit_button(name, disabled=False):
    btn = INPUT(_type="submit",_name=name, _id=name, _value="Submit HIT", _class="btn btn-primary btn-large")
    if disabled:
        btn['_disabled'] = 'disabled'
        
    return DIV(
        btn,
        BR(),
        SPAN("You may complete as many additional HITs in this group as you want.", _class="reminder-text")
    )

def uniquify(seq):
    # Dave Kirby
    # Order preserving uniquify
    # http://www.peterbe.com/plog/uniqifiers-benchmark (f8)
    seen = set()
    return [x for x in seq if x not in seen and not seen.add(x)]

def set_exclusion(groupName, excluderId):
    '''Sets up an exclusive relationship within a set of checkboxes. Useful for item1, item2, item3, none questions'''
    if not response.exclusions:
        response.exclusions = []
    response.exclusions.append((groupName, excluderId))

def randomize(name, questions):
    keys = None
    if session.randoms and session.randoms[name]:
        #retrieve an old order
        keys = session.randoms[name]
        
        #make sure it is consistent
        if len(keys) != len(questions):
            keys = None
    
    if not keys:
        #generate a new order
        keys = range(0, len(questions))
        random.shuffle(keys)
    
    #store the random order
    if not session.randoms:
        session.randoms = {}
    session.randoms[name] = keys
    
    orderedQuestions = []
    for index in keys:
        orderedQuestions.append(questions[index])
    
    return orderedQuestions
    
def verify_item(name):
    
    verificationIndex = hits_done(request.workerid, request.study)
    
    if not request.live and ("hits_completed" in request.vars):
        verificationIndex = int(request.vars.hits_completed)
        
    item = verifications[verificationIndex]
    answer = item["answer"]
    imgSrc = URL("static", "keystroke/verify/" + item["code"] + ".jpg")
    
    answerList = [answer]
    while len(answerList) < 5:
        verificationIndex += 7
        item = verifications[verificationIndex % len(verifications)]
        if item["answer"] not in answerList:
            answerList.append(item["answer"])
    
    random.shuffle(answerList)
    
    validators = [
        IS_NOT_EMPTY(error_message='You must identify the animal in the image'),
        IS_EQUAL_TO(answer, error_message='You did not select the correct animal!')
    ]
    
    verificationInputs = []
    
    for idx, answer in enumerate(answerList):
        animalId="ver-" + answer
        verificationInputs.append(
            LABEL(INPUT(_type="radio", _name=name, _value=answer, _id=animalId, requires=validators),
                answer, 
                _for=animalId, _class="radio")
            )
    
    verifyPic = IMG(_src=imgSrc)
    loading = DIV(verifyPic, _class="img-loading")
    
    verificationItem = form_item("Human check: Which animal is shown in the following image? (required)", verificationInputs, loading)
    return verificationItem

def form_item(prompt, inputs, *args):
    answers = DIV(_class="answers")
    
    if not isinstance(inputs, (list, tuple)):
        inputs = [inputs]
        
    for idx, input in enumerate(inputs):
        answers.append(input)

    question = DIV(_class="question")
    question.append(prompt)
    
    item = DIV(_class="item clearfix")
    item.append(question)
    item.append(answers)
    
    for arg in args:
        item.append(arg)
    
    return item

def auth_form(instructions, keyphrase):
    return FORM(
        DIV(instructions, _class="auth-instructions"),
        
        INPUT(_name="keyphrase", _type="hidden", _value=keyphrase),
        INPUT(_name="typing", _type="hidden", _id="typing-input"),
        
        DIV(keyphrase, _id="auth-example"),
        INPUT(_name="text", _type="text", _id="auth-field", _autocomplete="off", _value=""),
        
        INPUT(_name="submitbutton", _type="submit", _id="auth-submit", _class="btn btn-primary", _value="Submit"),
        DIV("analyzing typing patterns...", _class="loading", _style="display: none"),
        
        _id="auth-form", _method="post", _class="well form-inline")
    
def validate(typing, text, form):
    if not typing or not text:
        set_message(get_message('validateNotTyped'), 'error')
        record_action('no typing provided')
        #form.errors['text'] = get_message('validateNotTyped')
        return False

    typing = gluon.contrib.simplejson.loads(typing)
    keyphrase = KEYPHRASE

    # check for typos that the string matches
    typos = LD(keyphrase, text)
    
    # get statistics about the seeks and presses
    seeks, presses = distributions(typing)

    valid = True

    if len(text) * 2 > len(typing):
        set_message(get_message('validateNotTyped'), 'error')
        #form.errors['text'] = get_message('validateNotTyped')
        record_action('insufficient keypresses', len(typing))
        valid = False
    elif typos > MAX_TYPOS:
        set_message(get_message('validateTypos'), 'error')
        #form.errors['text'] = get_message('validateTypos')
        record_action('too many typos', typos)
        valid = False
    else:
        seek_stats = statistics(seeks)
        press_stats = statistics(presses)

        if not validStats(seek_stats):
            set_message(get_message('validateStats'), 'error')
            #form.errors['text'] = get_message('validateStats')
            record_action('invalid seek_stats', seek_stats)
            valid = False
        elif not validStats(press_stats):
            set_message(get_message('validateStats'), 'success')
            #form.errors['text'] = get_message('validateStats')
            record_action('invalid press_stats', press_stats)
            valid = False

    return valid

def prepareData(seeks, presses):
    data = {}
    bin_size = 2

    max_time = max(max(seeks), max(presses)) + bin_size
    max_time = max_time - (max_time % bin_size) # make it end on a bin
    for time in range(0, max_time, bin_size):
        data[time] = [str(time), 0, 0]

    for seek in seeks:
        time = seek - seek % bin_size
        data[time][1] += 1
    for press in presses:
        time = press - press % bin_size
        data[time][2] += 1

    values = []
    for key in sorted(data.iterkeys()):
        values.append(data[key])
    return values

def authorize(user_id):
    sleep_time = request.delay_time;
    time.sleep(sleep_time)
    if random.random() > request.reject_chance:
        return True
    else:
        return False

def validStats(stats):
    threshold = MIN_STDEV
    return stats["stdev"] > threshold

def LD(s,t):
    s = ' ' + s.lower()
    t = ' ' + t.lower()
    d = {}
    S = len(s)
    T = len(t)
    for i in range(S):
        d[i, 0] = i
    for j in range (T):
        d[0, j] = j
    for j in range(1,T):
        for i in range(1,S):
            if s[i] == t[j]:
                d[i, j] = d[i-1, j-1]
            else:
                d[i, j] = min(d[i-1, j] + 1, d[i, j-1] + 1, d[i-1, j-1] + 1)
    return d[S-1, T-1]

def distributions(typing):
    seekTimes = []
    pressTimes = []

    lastTime = 0
    for i, event in enumerate(typing):
        type = event["type"]
        time = event["time"]
        if type == "down":
            seekTimes.append(time - lastTime)
            lastTime = time
        elif type == "up":
            pressTimes.append(time - lastTime)
            lastTime = time
    return seekTimes, pressTimes

def statistics(values):

    mean = sum(values) / max(len(values), 1)
    variance = sum([(value - mean)**2 for value in values]) / max(len(values) - 1, 1)
    stdev = math.sqrt(variance)

    return dict(mean=mean, variance=variance, stdev=stdev)

def frequencies(values):
    freq = {}
    for v in values:
        if v not in freq:
            freq[v] = 0
        freq[v] = freq[v] + 1
    return freq


