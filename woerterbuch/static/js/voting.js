/** Voting via AJAX. */
var voting = {
    max_remember: 20,  // Number of votes to remember in localStorage

    // For a given word ID and up/down, find the vote link.
    find_link: function(wordid, up) {
        return $('.vote[data-wordid=' + wordid + '] a.' + (up ? 'up' : 'down'));
    },

    // Vote a particular word ID up or down.
    vote: function(wordid, up) {
        var clicked = voting.find_link(wordid, up);

        $.post(clicked.attr('href'), null,
            function(d, txt) {
                voting.store_vote(wordid, up);
                voting.mark_voted(clicked);
            });
    },

    // Store vote in localStorage
    store_vote: function(wordid, up) {
        if (!window.localStorage) return;  // Tough luck.

        var votes = voting.get_stored();
        if (!votes) {
            voting.set_stored([{w: wordid, u: up}]);
        } else {
            votes.push({w: wordid, u: up});
            while (votes.length > voting.max_remember) votes.shift();
            voting.set_stored(votes);
        }
    },

    // Get array of stored votes, null if none.
    get_stored: function() {
        var stored = window.localStorage.getItem('stored_votes');
        if (!stored)
            return stored;
        else
            return JSON.parse(stored);
    },

    // Set array of stored votes.
    set_stored: function(votes) {
        window.localStorage.setItem('stored_votes', JSON.stringify(votes));
    },

    // Mark a word voted-for, without actually submitting a vote.
    mark_voted: function(link) {
        link.addClass('clicked')
            .siblings('a').removeClass('clicked');
    }
};

$(function() {
    // Hook up voting via AJAX
    $('.vote a').click(function(e) {
        e.preventDefault();
        voting.vote($(this).parent().attr('data-wordid'),
            $(this).hasClass('up'));
        $(this).blur();
    });

    // Mark all remembered votes as such.
    (function() {
        if (!window.localStorage) return;

        var votes = voting.get_stored();
        for (i in votes) {
            var link = voting.find_link(votes[i]['w'], votes[i]['u']);
            voting.mark_voted(link);
        }
    })();
});
