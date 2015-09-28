/* globals jQuery, _, Backbone */
(function ($, _, Backbone) {
    'use strict';

    var MessageFormView = Backbone.View.extend({
        el: '#message-form form',
        events: {
            'submit': 'validate',
            'click .images .card-action a[data-image]': 'toggleImage'
        },
        initialize: function () {
            this.user = null;
            this.valid = false;
            this.encrypted = false;
            this.$imageInput = $('input[name="image"]', this.$el);
            this.$encyptButton = $('#encrypt-button', this.$el);
            this.$saveButton = $('#save-button', this.$el);
        },
        validate: function (e) {
            e.preventDefault();
        },
        toggleImage: function (e) {
            e.preventDefault();
            var $link = $(e.currentTarget),
                image = $link.data('image'),
                current = this.$imageInput.val();
            if (image === current) {
                $link.text($link.data('off'));
                this.$imageInput.val('');
            } else {
                $('a[data-image="' + current + '"]', this.$el)
                    .text($link.data('off'));
                $link.text($link.data('on'));
                this.$imageInput.val(image);
            }
        }
    });
    var form = new MessageFormView();

})(jQuery, _, Backbone);
