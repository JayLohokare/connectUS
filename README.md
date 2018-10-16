# ConnectUs - Platform for empowering immigrants and communities
Winner - 1st place at Global hack 2017 Saint Louis, Missouri

Project summary:
We noticed that most if not all of the problems that immigrants face are mainly due to lack of
Awareness and, Feeling of safety that comes by being with someone who we connect with

We hence thought of creating a solution that would help immigrants reach out to someone in times of needs. A platform that could foster local communities and help them go beyond geographic, lingual, economic and cultural boundaries.


1. We have created a system that seamlessly integrates with existing technologies (NO NEW APPS to be installed/Websites to be accessed by immigrants) to help communities connect with each other across multiple technological platforms. Some communities use Whatsapp, some use Facebook (others use other social media platforms). The divide between communities is not only ideological, but also technological. The immigrant/Refugee communities are already hesitant to open up to the world, even to their sister communities. The system we have implemented enables one click sharing of data, news, events, cultural uniqueness beyond such social media platforms and beyond physical boundaries -
Based on preferences, an immigrant can get updates from all over the world, from all social platforms into the platform of their choice. Imagine a refugee from Africa getting information about benefits, getting to know experience of people from other corner of the country/world. Imagine an American person getting information about all cultural richness of various immigrant communities on platform of his/her preference. The cross platform nature of this system allows communities to reach out to other communities, plan out events, help finding jobs, and learn to appreaciate each other. Those who are not tech-savy can get all the data from Whatsapp, Facebook, Linkedin, etc via SMS or even via voice mails (In language of choice)!

2. Multi-Lingual helpline that can be accessed through ANY platform. Ask questions, talk about worries, seek advice/guidance, get doubts cleared by simply sending a whatsapp message. Same applies for Facebook, Messenger, Linkedin (Any social media platform) or even SMS/MMS and calls! The interaction with this system is super easy - Input can be either of text, speech, image that too in any language/dialect. Ask questions to get immediate answers from our AI. If AI is unable to answer, the queries are forwarded to 'Community leaders/Patrons'. Get answers in audio/text (Any language of choice), with answers being customized for hyper-local requirements. The entire system is completely anonymous - At no stage is data stored on computers or with human. If AI is unable to solve a query, the query is sent out into out social community (Via the across social media platform). Verified and trust worthy person is allowed to answer the queries. At no stage is the person helping aware of who he is helping (So as to secure identity of the immigrant)

3. Portal for organizations to gain insights into behaviors, demands and requirements of immigrants through interactive dashboard and visualizations. Data collected through the communities (Via our social platform and query answering engine) is anonymized and made available so that organizations can use it for making policies to help immigrants/refugees

The system starts at chatbots built on all platforms, connected to single backend powered by Twilio. We exploited the programmatic voice and programmatic messages system part of twilio's free tier to build our ubiquitous chatbots (Based on every social media platforms, SMS, MMS, traditional calls). We use Google cloud platform to host our backend (written in Flask-Python) and to power our Natural Language processing and multi-lingual query processing. Our database, user management system is based on Firebase. 


Example usecase:
```
1. Geting help, answer questions - Language and platform independent
Immigrants can ask questions (Text/Audio) in any language to our system by messaging via any social media app (Whatapp, FB, WeChat, Viber, etc) or send SMS/MMS or call the AI helpline. All these end points are conencted to one AI that tries to extract information from the text/voice and see if it finds in connected database and APIs. If it finds an answer, the immigrant gets immediate reply. Else, the AI sends the query over to the community (sending the extracted text and voice message to community leader), without revealing identity of the immigrant. The community leader answers the query back to the system, which the system sends back to the immigrant. The system we built is platform and language independent!

2. Communities sharing posts to the world, irrespective of what platform they use
Communities have preference of social media platforms. Mexicans are actively posting queries on their respective FB groups, Indians have whatsapp groups, etc. The idea is to make experiences, achievements, events of such communities visible to entire world irrespective of platform.
Community leaders send posts(Events, achievements) to a chatbot on the platforms of their choice (Whatsapp, FB, WeChat, Viber, SMS, etc). The chatbot has numbers, social media IDs of all communities and their members. The chatbot phone number is also a part of the groups on these social apps. When chatbot receives messages from community leaders, it maps the events with target communities and sends out the post on all the platforms those communities are in.
Suppose an African community leader posts an event through Whatsapp, the chatbot will forward this post to all other groups (On whatsapp, FB, Viber, etc) relevant to the event (Relevance based on location, nationalty and language)
```

Technology used:
```
The chatbot, SMS and call interfaces are all powered by Twilio (This repo has all chatbot and voice interfaces). Twilio collects the messages and triggers an endpoint (REST) written in Python Flask. The Flask server then uses data extracted by twilio, data extracted from voice using GCP NLP to search for answers in database. We use spacy python library to find similarity in sentences. If similarity > 80%, the corresponding answer is returned as answer. Else, the flask app creates a new ID code (Created from immigrants phone number) and sends a message over all social platforms to relevant communities (Relevance decided by language and location). The community leaders receive a message from our system (Extracted text, audio) along with Chatbot deep link to send reply to. When the community leader sends answer, the system extracts targeted immigrant contact number from the ID code, and sends the answer back to immigrant. At no phase is a query mapped with immigrant stored on a sever or made available to community leaders, in order to secure immigrant identity.
Similar interface applies for sending events. posts accross various platforms. Community leaders can share selected posts/events to a chatbot availble on all platforms. The chatbot collects such posts from all platforms and sends them back to all community groups on their respective platforms. 
All data backend is based on Firebase
```

How to recreate the project:
```
Twilio - 
1. Create new calling number, connect the incoming endpoint to /voice (Flask app)
2. Create new whatsapp chatbot, connect incoming endpoint to /receiveWhatsapp (Flask app)
3. Same for SMS, other social apps

Firebase - 
Flask app has endpoints to register community leaders, immigrants, events, queries. 
The API auto creates Firebase DB structure

API - 
1. The API is based on Python-Flask.
2. python main.py to start the server
3. Use ngrox for tunneling to an globally accessible endpoint
4. ngrox http PORT(5000)
5. Use the ngrox endpoint on twilio
6. API can be hosted on GCP as well (Repo 2 is based on GCP)
```


This repo - Handles query handling pipeline (Get queries on any platform, AI/Community answers queries)

2nd repo - Social media broadcast (Forwarding events/posts to all social media platforms) - https://github.com/JayLohokare/twilio-boardcast-to-multiple-platforms

3rd repo - Dashboard to track activities of communities, common issues faced by immigrants, community stats mapped on dashboard - 
