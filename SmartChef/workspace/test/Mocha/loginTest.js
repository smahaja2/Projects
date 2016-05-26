var Browser = require('zombie');
Browser.site = 'http://localhost:8080/';
var assert = require('chai').assert;

describe('Chat testing', function(){
    this.timeout(5000);
    var browser = new Browser();

    before(function(done) {
        browser.visit("/events/10000/", done);
    });

    it('Chat box is visible to user', function(done){
        browser.assert.success();
        browser.assert.text('title', 'Your Event: Crossing Of Delaware');
        browser.assert.element('#chat-fixed');
        done();
    });

    it('Chat box welcomes user to chat upon load', function(done){
        browser.assert.success();
        browser.assert.text('title', 'Your Event: Crossing Of Delaware');
        browser.assert.element('#chat-fixed');

        var fixedContentText = browser.text('.fixedContent')
        assert.include(fixedContentText, 'connected to event chatroom 10000');
        done();
    });

    it('Submitting a message', function(done){
        var message = "zombie message";
        // TODO: submitting a message
        browser.fill('.userinput', 'zombie-test-message');

        //var event = new Event('keyup');
        //press enter
        //browser.fire('.userinput', event, function(){
            //console.log('user has entered a message');
            //var fixedContentText = browser.text('.fixedContent')
            //assert.include(fixedContentText, 'zombie-test-message');
        //});

        done();
    });

    describe('Chat testing - multiuser', function(){
        this.timeout(5000);
        var browser2 = new Browser();

        before(function(done) {
            browser2.visit("/events/10000/", done);
        });

        it('User 2 user enters chat', function(done){
            var fixedContentText = browser.text('.fixedContent')
            assert.include(fixedContentText, 'connected to event chatroom 10000');
            done();
        });

        describe('Chat testing - multiuser - exit', function(){
            this.timeout(5000);

            before(function(done) {
                browser2.close();
                done();
            });

            it('User 2 leaves chat', function(done){
                // TODO: another user leaves chat
                var fixedContentText = browser.text('.fixedContent')
                assert.include(fixedContentText, 'connected to event chatroom 10000');
                done();
            });
        });


    });

});