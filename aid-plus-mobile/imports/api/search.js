/**
 * Created by vasanthmahendran on 4/23/16.
 */
import { Mongo } from 'meteor/mongo';
 
export const RxTerms = new Mongo.Collection('rx_terms_fed');
export const Drugs = new Mongo.Collection('drug_fed');
export const NdfDrugs = new Mongo.Collection('ndf_drug_fed');
export const RxTermIng = new Mongo.Collection('rx_terms_ing_fed');

if (Meteor.isServer) {
    Meteor.publish('rxterms', function tasksPublication(search_term,skipCount) {
        var positiveIntegerCheck = Match.Where(function(x) {
            check(x, Match.Integer);
            return x >= 0;
        });
        check(skipCount, positiveIntegerCheck);
        var regExp = buildRegExp(search_term);
        var selector = {$or: [
            {BRAND_NAME: regExp},
            {FULL_NAME: regExp}
        ]};
        Counts.publish(this, 'resultCount', RxTerms.find(selector), {
            noReady: true
        });
        var options = {
            limit: 15,
            skip: skipCount
        };
        return RxTerms.find(selector, options);
    });
    
    Meteor.publish('rxterm',function rxtermdetailsPublication(rxcui){
        var rxterm = RxTerms.find({'RXCUI':rxcui});
        return rxterm;
    });
    Meteor.publish('rxterm_ing',function rxtermIngPublication(rxcui){
        var rxterm_ing = RxTermIng.find({'RXCUI': rxcui});
        return rxterm_ing;
    });
    Meteor.publish('ndfdrug',function ndfDrugPublication(rxcui){
        var rxterm_ing = RxTermIng.find({'RXCUI': rxcui})
        var ndf_drug
        if(rxterm_ing){
            var ings = [];
            rxterm_ing_fetch = rxterm_ing.fetch()
            for(var i = 0; i < rxterm_ing_fetch.length ; i++){
                ings.push(rxterm_ing_fetch[i].INGREDIENT.toLowerCase());
            }
            if(ings.length>0){
                ndf_drug = NdfDrugs.find({'name': {$in:ings}});
            }
        }
        return ndf_drug
    });
    Meteor.publish('drug',function drugPublication(rxcui){
        var rxterm = RxTerms.findOne({'RXCUI':rxcui});
        var drugs = Drugs.find({'drugname':rxterm.BRAND_NAME},{limit:15});
        return drugs;
    });
}
function buildRegExp(searchText) {
    // this is a dumb implementation
    var parts = searchText.trim().split(/[ \-\:]+/);
    return new RegExp("(" + parts.join('|') + ")", "ig");
}