/**
 * Created by vasanthmahendran on 4/22/16.
 */
import { Template } from 'meteor/templating';
import { RxTerms } from '../api/search.js';
import './list.html';
import './detail.js'

Router.route('/list/:search_term', function () {
    var search_term = this.params.search_term;
    var rxterms = RxTerms.find({});
    var startcount = (currentPage()-1)*15;
    var endcount = currentPage()*15;
    var totalcount = Counts.get('resultCount')
    this.render('list', {
        data: {
            rxterms: rxterms,
            search_term: search_term,
            startcount:startcount,
            endcount:endcount,
            totalcount:totalcount
        }
    });
},{name:'listpage'});

Template.main.events({
    'submit .navsearchform'(event) {
        event.preventDefault();
        Router.go('listpage',{ search_term: event.target.navsearchformtext.value });
    },
});

Template.list.onCreated( function() {
    template = this;
    template.autorun(function() {
        var search_term = Router.current().params.search_term;
        var skipCount = (currentPage() - 1) * 15;
        template.subscribe('rxterms',search_term,skipCount);
    });


});
var currentPage = function() {
    return parseInt(Router.current().params.query.page) || 1;
}
var hasMorePages = function() {
    var totalresults = Counts.get('resultCount');
    return currentPage() * parseInt(15) < totalresults;
}

Template.list.helpers({
    prevPage: function() {
        var search_term = Router.current().params.search_term;
        var previousPage = currentPage() === 1 ? 1 : currentPage() - 1;
        return Router.routes.listpage.path({search_term: search_term},{query:'page='+previousPage});
    },
    nextPage: function() {
        var search_term = Router.current().params.search_term;
        var nextPage = hasMorePages() ? currentPage() + 1 : currentPage();
        return Router.routes.listpage.path({search_term: search_term},{query:'page='+nextPage});
    },
    prevPageClass: function() {
        return currentPage() <= 1 ? "disabled" : "";
    },
    nextPageClass: function() {
        return hasMorePages() ? "" : "disabled";
    }
});
//Template.list.events({
//   "click .prevPage": function( event, template ) {
//        var search_term = Router.current().params.search_term;
//        var previousPage = currentPage() === 1 ? 1 : currentPage() - 1;
        //Router.go('listpage',{ search_term:search_term},{query:'page='+previousPage});
        //document.location.reload(true);
//    },
//    "click .nextPage": function( event, template ) {
//        var search_term = Router.current().params.search_term;
//        var nextPage = hasMorePages() ? currentPage() + 1 : currentPage();
        //Router.go('listpage',{ search_term:search_term },{query:'page='+nextPage});
        //document.location.reload(true);
//    }
//});