var frisby = require('frisby');
frisby.create('EventsHub should be up')
    .get('http://localhost:8080/')
    .expectStatus(200)
    .expectHeaderContains('content-type', 'text/html')
    .expectBodyContains('Welcome to SmartChef!')
    .toss();

