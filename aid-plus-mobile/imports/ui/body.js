/**
 * Created by vasanthmahendran on 4/23/16.
 */
import { Template } from 'meteor/templating';
import './body.html';
import './list.js'

Router.route('/search');

Router.route('/',{
  name: 'home',
  template:'search'
});

/*Router.route('/list/:search_term', {
  name:'listpage',
  template: 'list',
  data: {
    rxterms: function(){
      var search_term_var = Router.current().params.search_term;
      return RxTerms.find({'INGREDIENT':{$regex : ".*"+search_term_var+".*"}});
    }
  }
});*/

Router.configure({
  layoutTemplate: 'main'
});

Template.search.events({
  'submit .new-task'(event) {
    event.preventDefault();
    Router.go('listpage',{ search_term: event.target.text.value });
  },
});

Template.main.events({
    'submit .navsearchform'(event) {
        event.preventDefault();
        Router.go('listpage',{ search_term: event.target.navsearchformtext.value });
    },
});
