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
                voting.mark_voted(clicked, true);
            });
    },

    // Store vote in localStorage
    store_vote: function(wordid, up) {
        if (!window.localStorage) return;  // Tough luck.

        var votes = voting.get_stored();
        if (!votes) votes = {}
        votes[wordid] = {u: up, d: new Date().getTime()};
        while (Object.keys(votes).length > voting.max_remember) {
            var dates = {};
            for (w in votes) dates[votes[w]['d']] = w;  // Map date -> word
            var mindate = Math.min.apply(Math, Object.keys(dates));
            delete votes[dates[mindate]];
        }
        voting.set_stored(votes);
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
    mark_voted: function(link, fix_counts) {
        var other_link = link.siblings('a:eq(0)'),
            counts = link.siblings('.counts');

        if (fix_counts) {
            // Increment this link.
            if (!link.hasClass('clicked'))
                voting.change_count(counts, link.hasClass('up') ? 'up' : 'down', 1)

            // Decrement the other, if necessary.
            if (other_link.hasClass('clicked'))
                voting.change_count(counts, other_link.hasClass('up') ? 'up' : 'down', -1)
        }

        link.addClass('clicked');
        other_link.removeClass('clicked');
    },

    // Increment/decrement a count number
    change_count: function(counts, direction, amount) {
        var count = counts.find('.' + direction),
            num = parseInt(count.text());
        count.text(num + amount);
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
            var link = voting.find_link(i, votes[i]['u']);
            voting.mark_voted(link, false);
        }
    })();
});
