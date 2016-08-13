/**
 * Created by vasanthmahendran on 4/23/16.
 */
import { RxTerms } from '../api/search.js';
import { Drugs } from '../api/search.js';
import { NdfDrugs } from '../api/search.js';
import { RxTermIng } from '../api/search.js';
import './detail.html';

Router.route('/details/:rxcui', function () {
    var rxcui = this.params.rxcui.toString();
    var rxterm = RxTerms.findOne({'RXCUI':rxcui});
    var rxterm_ing = RxTermIng.find({'RXCUI': rxcui});
    var ndf_drug = NdfDrugs.find({});
    var drug_cursor = Drugs.find({});
    this.render('details', {
        data: {
            rxterm: rxterm,
            rxterm_ing:rxterm_ing,
            drug_cursor: drug_cursor,
            ndfdrug: ndf_drug
        }
    });
},{name:'detailpage'});

Template.main.events({
    'submit .navsearchform'(event) {
        event.preventDefault();
        Router.go('listpage',{ search_term: event.target.navsearchformtext.value });
    },
});
Template.registerHelper("isEmpty", function (object) {
    return jQuery.isEmpty(object);
});

Template.details.onCreated( function() {
    var rxcui = Router.current().params.rxcui.toString();
    this.subscribe('rxterm',rxcui);
    this.subscribe('ndfdrug',rxcui);
    this.subscribe('drug',rxcui);
    this.subscribe('rxterm_ing',rxcui);
});