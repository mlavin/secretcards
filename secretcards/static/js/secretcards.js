/* globals jQuery, _, Backbone, kbpgp */
(function ($, _, Backbone, kbpgp) {
    'use strict';

    var ResultsItemView = Backbone.View.extend({
        tagName: 'li',
        events: {
            'click a': 'selected'
        },
        template: _.template(
            '<a href="#" class="row">' +
            '<span class="col s6 l10">' +
            '<%- username %> <% if (name) { %>(<%- name %>)<% } %>' +
            '</span>' +
            '<span class="col s6 l2">' +
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
            this.trigger('clear');
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
            selectedView.render();
            selectedView.on('clear', this.clear, this);
            this.trigger('selected', item);
        },
        clear: function () {
            this.trigger('clear');
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
            this.resultsView.on('clear', this.removeKey, this);
            this.resultsView.render();
        },
        fetchKey: function (info) {
            var self = this;
            $.get('https://keybase.io/' + info.username + '/key.asc')
                .done(function (key) {
                    self.trigger('selected', key);
                });
        },
        removeKey: function () {
            this.trigger('selected', null);
        }
    });

    var MessageFormView = Backbone.View.extend({
        el: '#message-form form',
        events: {
            'submit': 'submit',
            'click .images .card': 'toggleImage',
            'input :input[name="message"]': 'toggleEncryptButton',
            'click #encrypt-button': 'encryptMessage'
        },
        initialize: function () {
            this.key = null;
            this.encrypted = false;
            this.$imageInput = $(':input[name="image"]', this.$el);
            this.$messageInput = $(':input[name="message"]', this.$el);
            this.$encryptButton = $('#encrypt-button', this.$el);
            this.$saveButton = $('#save-button', this.$el);
        },
        valid: function () {
            return this.encrypted && this.$imageInput.val();
        },
        toggleImage: function (e) {
            e.preventDefault();
            var $link = $('.card-action a[data-image]', e.currentTarget),
                image = $link.data('image'),
                current = this.$imageInput.val();
            if (image === current) {
                $link.text($link.data('off'));
                $link.parents('.card').removeClass('z-depth-5');
                this.$imageInput.val('');
            } else {
                $('a[data-image="' + current + '"]', this.$el)
                    .text($link.data('off'))
                    .parents('.card').removeClass('z-depth-5');
                $link.text($link.data('on'));
                $link.parents('.card').addClass('z-depth-5');
                this.$imageInput.val(image);
            }
            this.toggleSaveButton();
        },
        toggleEncryptButton: function () {
            this.$encryptButton.prop('disabled', true);
            this.$encryptButton.addClass('disabled');
            this.$encryptButton.removeClass('waves-effect waves-green');
            if (this.key !== null && this.$messageInput.val() && !this.encrypted) {
                this.$encryptButton.prop('disabled', false);
                this.$encryptButton.removeClass('disabled');
                this.$encryptButton.addClass('waves-effect waves-green');
            }
        },
        toggleSaveButton: function () {
            if (this.valid()) {
                this.$saveButton.prop('disabled', false);
                this.$saveButton.removeClass('disabled');
            } else {
                this.$saveButton.prop('disabled', true);
                this.$saveButton.addClass('disabled');
            }
        },
        populateKey: function (key) {
            var self = this;
            if (key === null) {
                this.key = key;
                if (this.encrypted) {
                    this.$messageInput.val('');
                    this.$messageInput.prop('disabled', false);
                    this.$messageInput.removeClass('disabled');
                    this.encrypted = false;
                }
                this.toggleEncryptButton();
            } else {
                kbpgp.KeyManager.import_from_armored_pgp({
                    armored: key
                }, function (error, keyManager) {
                    if (!error) {
                        self.key = keyManager;
                        self.toggleEncryptButton();
                    } else {
                        self.populateKey(null);
                    }
                });
            }
        },
        encryptMessage: function (e) {
            e.preventDefault();
            var message = this.$messageInput.val(),
                self = this;
            if (this.key !== null && !this.encrypted && message) {
                kbpgp.box({msg: message, encrypt_for: this.key}, function (error, result) {
                    if (result && !error) {
                        self.encrypted = true;
                        self.$messageInput.val(result);
                        self.$messageInput.prop('disabled', true);
                        self.$messageInput.addClass('disabled');
                        self.toggleEncryptButton();
                        self.toggleSaveButton();
                    }
                });
            }
        },
        submit: function (e) {
            if (this.valid()) {
                this.$messageInput.prop('disabled', false);
            } else {
                e.preventDefault();
            }
        }
    });
    var keybase = new KeybaseView();
    var form = new MessageFormView();
    keybase.on('selected', form.populateKey, form);

})(jQuery, _, Backbone, kbpgp);
