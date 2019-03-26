console.log('js loaded.')

// bind click event to record form submit buttons
$(document).ready(function () {
    $("[id$=_mlt_btn]").click(function () {
        let doc_id = this.id.split("_")[0]

        if ($("#" + doc_id + "_mlt_content").children().length == 0) {
            // if children (similar documents), get more like this
            var self = $(this).append("<img class='pl-2' src='/static/loading.gif'>"); // change button html to loading gif
            setTimeout(function () {
                $.post('/more_like_this', {
                        'doc_id': doc_id,
                        'index': this.value
                    }) // submit post request
                    .done(function (response) {
                        console.log(response)
                        for (let i = 0; i < response.length; i++) {
                            let title = response[i]['_source']['title']
                            let index = response[i]['_index']
                            let rec_id = response[i]["_id"]
                            if (index == 'projects') {
                                html_string = `<h6 class='w-100 align-middle text-nowrap' style='overflow:hidden; text-overflow:ellipsis;'>
                                <span class='badge primary-color-dark text-capitalize z-depth-0 mr-1'>Project</span>
                                <a>` + title + `</a></h6>`
                            } else if (index == 'publications') {
                                html_string = `<h6 class='w-100 align-middle text-nowrap' style='overflow:hidden; text-overflow:ellipsis;'>
                                <span class='badge deep-purple darken-4 text-capitalize z-depth-0 mr-1'>Publication</span>
                                <a>` + title + `</a></h6>`
                            }
                            $("#" + doc_id + "_mlt_content").append(html_string)
                            // add record if does not already exist in DOM
                            if ($("#" + rec_id).length) {
                                console.log("exists.")
                                // addModal(rec_id, doc_id)
                            } else {
                                console.log("does not exist.")
                            }
                        }
                    }).fail(function () {
                        alert('Failed to find more like this.')
                    });
                self.html('More Like This');
            }, 1000);
            // toggle collapse content
            $("#" + doc_id + "_mlt_content").collapse('toggle')
        } else {
            // toggle collapse content
            $("#" + doc_id + "_mlt_content").collapse('toggle')
        }

        return false;
    })
});

function addModal(rec_id, doc_id) {
    var modal = $("#"+doc_id); // modal to copy
    let clone = modal.clone(); // create copy 
    let desc = clone.find("[id^="+doc_id+"]") // get all descendants w/ doc_id

    // first change all ids
    clone[0].id = rec_id; // change id
    for (let i = 0; i < desc.length; i++) {
        let id = desc[i].id // get old id
        let parts = id.split("_")
        parts[0] = rec_id // change record id
        new_id = parts.join("_") // create new id
        desc[i].id = new_id // update descendant id
    }
    // console.log(desc)
    // next update modal content
    clone.attr('class',"modal fade")
    clone.find("#"+rec_id+"_title").text("Test") // title
    clone.find("#"+rec_id+"_record_type").text("Test") // record type
    clone.find("#"+rec_id+"_tags").html("Test") // record tags
    clone.find("#"+rec_id+"_elem_tags").html("Test") // record element tags
    clone.find("#"+rec_id+"_abstract").text("Test") // abstract
    clone.find("#"+rec_id+"_status").text("Test") // status
    clone.find("#"+rec_id+"_funding").text("Test") // funding
    clone.find("#"+rec_id+"_fundagencies").text("Test") // funding agencies
    clone.find("#"+rec_id+"_perfagencies").text("Test") // performing agencies
    clone.find("#"+rec_id+"_startdate").text("Test") // start date
    clone.find("#"+rec_id+"_compdate").text("Test") // completion date
    clone.find("#"+rec_id+"_urls").text("Test") // funding
    clone.appendTo("#modals") // append new modal
}


// bind click event to bookmark buttons
$(document).ready(function () {
    $("[id$=_bookmark_btn]").click(function () {
        let doc_id = this.id.split("_")[0]
        let marked = $(this).hasClass('unmarked')
        if (marked) {
            // document was bookmarked
            $("#" + doc_id + "_bookmark_icon").attr('class', 'fa fa-bookmark fa-lg pr-1');
            $("#" + doc_id + "_bookmark_text").html('Marked');
            $(this).addClass('marked').removeClass('unmarked');
            $("#" + doc_id + "_modal_bookmark_icon").attr('class', 'fa fa-bookmark fa-lg pr-1');
            $("#" + doc_id + "_modal_bookmark_text").html('Marked');
            $("#" + doc_id + "_modal_bookmark_btn").addClass('marked').removeClass('unmarked');
        } else {
            //  document was unmarked
            $("#" + doc_id + "_bookmark_icon").attr('class', 'fa fa-bookmark-o fa-lg pr-1');
            $("#" + doc_id + "_bookmark_text").html('Bookmark');
            $(this).addClass('unmarked').removeClass('marked');
            $("#" + doc_id + "_modal_bookmark_icon").attr('class', 'fa fa-bookmark-o fa-lg pr-1');
            $("#" + doc_id + "_modal_bookmark_text").html('Bookmark');
            $("#" + doc_id + "_modal_bookmark_btn").addClass('unmarked').removeClass('marked');
        }
        $.post('/update/record/bookmark', {
                'doc_id': doc_id,
                'index': this.value,
                'marked': marked
            }) // submit post request
            .done(function () {
                return false
            }).fail(function () {
                alert('Failed to bookmark record.')
            });
    })
});

//  bind click event to DB update button
$(document).ready(function () {
    $("#update-database").click(function () {
        $("#loading-text").html('Updating local database. This could take several minutes...')
        $("#loading").show()
        setTimeout(function () {
            $.post('/update/database') // submit post request
                .done(function (response) {
                    $("#loading-text").html('Success!')
                    setTimeout(function () {
                        $("#loading").hide()
                    }, 5000);
                }).fail(function () {
                    // $("#loading-spinner").hide()
                    $("#loading-text").html('Error: Could not update database.')
                    setTimeout(function () {
                        $("#loading").hide()
                    }, 3000);
                });
        }, 2000);
    })
});

// bind click event to record form submit buttons
$(document).ready(function () {
    $("[id$=_submit]").click(function () {
        let doc_id = this.id.split("_")[0]
        var formData = $('#' + doc_id + '_form').serialize() // get form data
        var self = $(this).html("<img src='/static/loading.gif'>"); // change button html to loading gif
        setTimeout(function () {
            $.post('/update/record/annotate', formData) // submit post request
                .done(function (response) {
                    return false
                }).fail(function () {
                    alert('Failed to apply changes.')
                });
            self.html('Apply');
        }, 1000);
        return false;
    })
});


function toggleCollapse() {

    var isCollapsed = (
        document.getElementById("collapse-icon").className == "fa fa-plus-circle"
    )

    if (isCollapsed != true) {

        document.getElementById("collapseOne").className = "collapse";
        document.getElementById("collapseTwo").className = "collapse";
        document.getElementById("collapseThree").className = "collapse";
        document.getElementById("collapse-icon").className = "fa fa-plus-circle";

    } else {

        document.getElementById("collapseOne").className = "collapse show";
        document.getElementById("collapseTwo").className = "collapse show";
        document.getElementById("collapseThree").className = "collapse show";
        document.getElementById("collapse-icon").className = "fa fa-minus-circle";

    }
}


function disableRecordTypeOption() {
    document.getElementById("rt3").disabled = true
}

function disableStatus() {
    document.getElementById("status").disabled = true
}

function enableStatus() {
    document.getElementById("status").disabled = false
}

function setSortOption(docType) {
    if (docType == 'project') {
        document.getElementsByName("sortBy")[0].options[2].text = "Start Date"
    } else if (docType == 'publication') {
        document.getElementsByName("sortBy")[0].options[2].text = "Publication Date"
    }
}

function setButtonState(buttonStates) {

    let search_type = buttonStates.type
    let topic = buttonStates.topic
    let element = buttonStates.element
    let docType = buttonStates.doc_type
    let status = buttonStates.status
    let dateRange = buttonStates.date_range
    let sortBy = buttonStates.sort_by
    let rpp = buttonStates.rpp

    console.log(search_type)

    // update 'topic' selection
    if (topic == 'all') {
        document.getElementsByName('topic')[0].options.selectedIndex = 1
    } else if (topic == 'construction_quality') {
        document.getElementsByName('topic')[0].options.selectedIndex = 2
    } else if (topic == 'design_and_details') {
        document.getElementsByName('topic')[0].options.selectedIndex = 3
    } else if (topic == 'material_specifications') {
        document.getElementsByName('topic')[0].options.selectedIndex = 4
    } else if (topic == 'live_load') {
        document.getElementsByName('topic')[0].options.selectedIndex = 5
    } else if (topic == 'environment') {
        document.getElementsByName('topic')[0].options.selectedIndex = 6
    } else if (topic == 'maintenance_and_preservation') {
        document.getElementsByName('topic')[0].options.selectedIndex = 7
    } else if (topic == 'structural_integrity') {
        document.getElementsByName('topic')[0].options.selectedIndex = 8
    } else if (topic == 'structural_condition') {
        document.getElementsByName('topic')[0].options.selectedIndex = 9
    } else if (topic == 'functionality') {
        document.getElementsByName('topic')[0].options.selectedIndex = 10
    } else if (topic == 'cost') {
        document.getElementsByName('topic')[0].options.selectedIndex = 11
    }


    // update 'element' selection
    if (element == 'all') {
        document.getElementsByName('element')[0].options.selectedIndex = 1
    } else if (element == 'superstructure') {
        document.getElementsByName('element')[0].options.selectedIndex = 2
    } else if (element == 'untreated_deck') {
        document.getElementsByName('element')[0].options.selectedIndex = 3
    } else if (element == 'treated_deck') {
        document.getElementsByName('element')[0].options.selectedIndex = 4
    } else if (element == 'joints') {
        document.getElementsByName('element')[0].options.selectedIndex = 5
    } else if (element == 'bearings') {
        document.getElementsByName('element')[0].options.selectedIndex = 6
    } else if (element == 'coatings') {
        document.getElementsByName('element')[0].options.selectedIndex = 7
    } else if (element == 'prestressing') {
        document.getElementsByName('element')[0].options.selectedIndex = 8
    }

    //  update record type selection
    if (docType == 'project') {
        document.getElementById('rt2').checked = true
        setSortOption(docType)
        enableStatus()
        if (search_type == 'click_map') {
            disableRecordTypeOption()
        }
    } else {
        document.getElementById('rt3').checked = true
        setSortOption(docType)
        disableStatus()
    }



    // update status selection
    if (status == 'all') {
        document.getElementsByName('status')[0].options.selectedIndex = 1
    } else if (status == 'active') {
        document.getElementsByName('status')[0].options.selectedIndex = 2
    } else if (status == 'completed') {
        document.getElementsByName('status')[0].options.selectedIndex = 3
    } else if (status == 'programmed') {
        document.getElementsByName('status')[0].options.selectedIndex = 4
    } else if (status == 'proposed') {
        document.getElementsByName('status')[0].options.selectedIndex = 5
    }

    // update date range selection
    if (dateRange == '1') {
        document.getElementById('dr1').checked = true
    } else if (dateRange == '5') {
        document.getElementById('dr2').checked = true
    } else if (dateRange == '50') {
        document.getElementById('dr3').checked = true
    }

    // update rpp selection
    if (rpp == '5') {
        document.getElementById('rpp1').checked = true
    } else if (rpp == '10') {
        document.getElementById('rpp2').checked = true
    }

    // update sort selection
    if (sortBy == 'score') {
        document.getElementsByName('sortBy')[0].options.selectedIndex = 1
    } else if (sortBy == 'date') {
        document.getElementsByName('sortBy')[0].options.selectedIndex = 2
    } else if (sortBy == 'both') {
        document.getElementsByName('sortBy')[0].options.selectedIndex = 3
    }

}

let page = "{{ page|safe }}"
if (page == '1') {
    document.getElementById("leftArrow1").className = "page-item disabled mr-1"
    document.getElementById("leftArrow2").className = "page-item disabled mr-1"
    document.getElementById("leftArrow3").className = "page-item disabled mr-1"
}