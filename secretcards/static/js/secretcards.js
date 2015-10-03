/* globals jQuery, _, Backbone */
(function ($, _, Backbone) {
    'use strict';

    var ResultsItemView = Backbone.View.extend({
        tagName: 'li',
        events: {
            'click a': 'selected'
        },
        template: _.template(
            '<a href="#" class="row">' +
            '<span class="col s10">' +
            '<%- username %> <% if (name) { %>(<%- name %>)<% } %>' +
            '</span>' +
            '<span class="col s2">' +
            '<% if (thumbnail) { %>' +
            '<img src="<%- thumbnail %>" alt="<%- username %>" class="circle responsive-img">' +
            '<% } %>' +
            '</span>' +
            '</a>'),
        initialize: function (options) {
            this.info = options.info;
        },
        render: function () {
            this.$el.html(this.template(this.info));
        },
        selected: function (e) {
            e.preventDefault();
            this.trigger('selected', this.info);
        }
    });

    var SelectedItemView = Backbone.View.extend({
        tagName: 'div',
        className: 'chip',
        template: _.template(
            '<% if (thumbnail) { %>' +
            '<img src="<%- thumbnail %>" alt="<%- username %>">' +
            '<% } %>' +
            '<%- username %> <% if (name) { %>(<%- name %>)<% } %>' +
            '<i class="material-icons">close</i>'),
        events: {
            'click i': 'close'
        },
        initialize: function (options) {
            this.info = options.info;
            this.parent = options.parent;
            this.parent.after(this.$el);
            this.$el.css({
                position: 'absolute',
                left: parseFloat(this.parent.css('margin-left')) + 12,
                top: 6
            });
        },
        render: function () {
            this.parent.data('placeholder', this.parent.attr('placeholder'));
            this.parent.attr('placeholder', '');
            this.parent.val('');
            this.parent.prop('disabled', true);
            this.$el.html(this.template(this.info));
        },
        close: function (e) {
            e.preventDefault();
            this.parent.attr('placeholder', this.parent.data('placeholder'));
            this.parent.prop('disabled', false);
            this.parent.focus();
            this.remove();
        }
    });

    var ResultsView = Backbone.View.extend({
        tagName: 'ul',
        className: 'dropdown-content keybase-results',
        initialize: function (options) {
            var self = this;
            this.results = options.results;
            this.parent = options.parent;
            this.parent.after(this.$el);
            this.$el.css({
                position: 'absolute',
                left: this.parent.position().left + parseFloat(this.parent.css('margin-left')),
                top: this.parent.position().top + this.parent.height(),
                width: this.parent.outerWidth()
            });
            this.parent.on('blur', function () {
                window.setTimeout(function () {
                    self.remove();
                }, 100);
            });
        },
        render: function () {
            _.each(this.results, function (item) {
                var view = new ResultsItemView({info: item});
                this.on('remove', view.remove, view);
                view.on('selected', this.selected, this);
                this.$el.append(view.$el);
                view.render();
            }, this);
            this.$el.addClass('active');
            this.$el.animate({opacity: 1}, {queue: false, duration: 100, easing: 'easeOutSine'})
                .slideDown({queue: false, duration: 200, easing: 'easeOutCubic'});
        },
        remove: function () {
            this.trigger('remove');
            Backbone.View.prototype.remove.call(this);
        },
        selected: function (item) {
            var selectedView = new SelectedItemView({info: item, parent: this.parent});
            this.trigger('selected', item);
            selectedView.render();
        }
    });

    var KeybaseView = Backbone.View.extend({
        el: '#message-form .row.keybase',
        events: {
            'input #keybase': 'queueSearch'
        },
        initialize: function () {
            this.selected = false;
            this.timer = null;
            this.$input = $('#keybase', this.$el);
            this.$spinner = $('.preloader-wrapper', this.$el);
            this.resultsView = null;
        },
        queueSearch: function (e) {
            var value = this.$input.val();
            if (this.timer) {
                window.clearTimeout(this.timer);
            }
            if (value.length > 2) {
                this.$spinner.addClass('active');
                this.timer = window.setTimeout(_.bind(this.search, this), 200);
            }
        },
        search: function () {
            var value = this.$input.val(),
                spinner = this.$spinner;
            $.get('https://keybase.io/_/api/1.0/user/autocomplete.json', {q: value})
                .done(_.bind(this.results, this))
                .always(function () {
                    spinner.removeClass('active');
                });
        },
        results: function (data) {
            var results = _.map(data.completions || [], function (result) {
                return {
                    name: (result.components.full_name && result.components.full_name.val) || '',
                    username: result.components.username.val,
                    thumbnail: result.thumbnail
                };
            });
            if (this.resultsView) {
                this.resultsView.remove();
            }
            this.resultsView = new ResultsView({results: results, parent: this.$input});
            this.resultsView.on('selected', this.fetchKey, this);
            this.resultsView.render();
        },
        fetchKey: function (info) {
            var self = this;
            $.get('https://keybase.io/' + info.username + '/key.asc')
                .done(function (key) {
                    self.trigger('selected', key);
                });
        }
    });

    var MessageFormView = Backbone.View.extend({
        el: '#message-form form',
        events: {
            'submit': 'validate',
            'click .images .card-action a[data-image]': 'toggleImage',
            'input :input[name="message"]': 'toggleEncryptButton'
        },
        initialize: function () {
            this.key = null;
            this.valid = false;
            this.encrypted = false;
            this.$imageInput = $('input[name="image"]', this.$el);
            this.$encryptButton = $('#encrypt-button', this.$el);
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
        },
        toggleEncryptButton: function () {
            if (this.key !== null && $(':input[name="message"]', this.$el).val()) {
                this.$encryptButton.prop('disabled', false);
                this.$encryptButton.removeClass('disabled');
            } else {
                this.$encryptButton.prop('disabled', true);
                this.$encryptButton.addClass('disabled');
            }
        },
        toggleSaveButton: function () {

        },
        populateKey: function (key) {
            this.key = key;
            this.toggleEncryptButton();
        }
    });
    var keybase = new KeybaseView();
    var form = new MessageFormView();
    keybase.on('selected', form.populateKey, form);

})(jQuery, _, Backbone);
