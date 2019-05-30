console.log('js loaded.')

// bind click event to add tag
function bindClick_tag_add() {
    $(document).ready(function () {
        $("[id^=add-]").click(function () {

            let tag = this.id.split("-")[1]
            let index = this.id.split("-")[2]
            let doc_id = this.id.split("-")[3]

            // first submit post request to remove tag from record in DB
            $.post("/update/record/add_tag", {
                'doc_id': doc_id,
                'index': index,
                'tag': tag
            }).done(function () {
                return false
            }).fail(function () {
                alert('Failed to add tag to record.')
            });

            
            // add tag to record modal
            var className = this.rel==1 ? "badge teal darken-2 z-depth-1 p-2 mr-1 mt-1" : "badge orange darken-4 z-depth-1 p-2 mr-1 mt-1"
            let modal_tag = $("<h4><span></span></h4>")
                .attr({id:[index, doc_id, tag, 'tag'].join('-')})
                .addClass("d-inline")
                .find("span")
                .addClass(className)
                .html(this.text)
                .append($("<i></i>")
                .attr({style:"line-height:18px; font-size: 1.0rem;"})
                .addClass("close fa fa-times pt-0 pl-2 pr-0 text-white"))
                .end()
              
            if (this.rel == 1) {
                modal_tag.appendTo("#"+doc_id+"_tags")
            } else {
                modal_tag.appendTo("#"+doc_id+"_elem_tags")
            }

            // add tag to record card 
            var className = this.rel==1 ? "badge teal darken-2 z-depth-1 text-capitalize p-2 mr-1 mt-1" : "badge orange darken-4 z-depth-1 text-capitalize p-2 mr-1 mt-1"
            let card_tag = $("<h6><span></span></h6>")
                .attr({id: [index, doc_id, tag, 'tag_card'].join('-')})
                .addClass("d-inline")
                .find("span")
                .addClass(className)
                .html(this.text)
                .end()

            if (this.rel == 1) {
                card_tag.appendTo("#card_"+doc_id+"_tags")
            } else if (this.rel==2){
                console.log(this.rel)
                card_tag.appendTo("#card_"+doc_id+"_elem_tags")
            }

            // bind delete button click event
            bindClick_tag_delete()
            return false;
        })
    });
}
bindClick_tag_add()

// bind click event to remove tag
function bindClick_tag_delete() {
    $(document).ready(function () {
        $("[id$=-tag]").click(function () {

            let index = this.id.split("-")[0]
            let doc_id = this.id.split("-")[1]
            let tag = this.id.split("-")[2]
            // alert(doc_id + " and " + tag + " and " + index);
            
            // first submit post request to remove tag from record in DB
            $.post("/update/record/remove_tag", {
                'doc_id': doc_id,
                'index': index,
                'tag': tag
            }).done(function () {
                return false
            }).fail(function () {
                alert('Failed to remove tag from record.')
            });

            // on success, remove tag from modal
            this.remove();
            // next remove tag from card
            $("#" + this.id + "_card").remove();

            return false;
        })
    });
}
bindClick_tag_delete()

// bind click event to record titles
$("[id$=_click_title]").click(function () {
    $("[id^=back_to]").remove()
})

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


// bind click event to MLT button
function bindClick_MLT_button() {
    $("[id$=_mlt_btn]").unbind('click')
    $("[id$=_mlt_btn]").click(function () {
        let source_id = this.id.split("_")[0] // current modal id
        let ind = this.name
        if ($("#" + source_id + "_mlt_content").children().length == 0) {
            // if children (similar documents), get more like this
            var self = $(this).append("<img class='pl-2' src='/static/loading.gif'>"); // change button html to loading gif
            setTimeout(function () {
                $.post('/more_like_this', {
                        'doc_id': source_id,
                        'index': ind
                    }) // submit post request
                    .done(function (response) {
                        for (let i = 0; i < response.length; i++) {
                            let title = response[i]['_source']['title']
                            let index = response[i]['_index']
                            let target_id = response[i]["_id"] // target modal id
                            if (index == 'projects') {
                                html_string = `<h6 class='w-100 align-middle text-nowrap' style='overflow:hidden; text-overflow:ellipsis;'>
                                <span class='badge primary-color-dark text-capitalize z-depth-0 mr-1'>Project</span>
                                <a id='link_to_` + target_id + `'>` + title + `</a></h6>`
                            } else if (index == 'publications') {
                                html_string = `<h6 class='w-100 align-middle text-nowrap' style='overflow:hidden; text-overflow:ellipsis;'>
                                <span class='badge deep-purple darken-4 text-capitalize z-depth-0 mr-1'>Publication</span>
                                <a id='link_to_` + target_id + `'>` + title + `</a></h6>`
                            }
                            $("#" + source_id + "_mlt_content").append(html_string)

                            // add record modal if does not already exist in DOM
                            if ($("#" + target_id).length) {
                                // console.log(target_id+" exists.")
                            } else {
                                addModal(response[i]['_source'], target_id, source_id)
                            }

                            // bind click event to mlt titles
                            $("[id$=_" + target_id + "]").click(function () {
                                // on click, hide current modal, show new modal
                                $("#" + source_id).modal("toggle")
                                $("#" + target_id).modal("toggle")
                                $("#" + target_id).css('overflow-y', 'auto');
                                // remove/add back button to target modal
                                $("#" + target_id + "_modal_header").find("[id^=back_to_]").remove()
                                $("#" + target_id + "_modal_header").prepend(
                                    `<div class="d-inline pl-4" id="back_to_` + source_id + `">
                                        <a><i class="fa fa-chevron-left fa-lg" aria-hidden="true"></i></a>        
                                    </div>`
                                )
                                // bind click event to back button of target modal
                                $("#" + target_id + "_modal_header").find("#back_to_" + source_id).find("a").click(function () {
                                    // send current modal id to new modal back button
                                    $("#" + target_id).modal("toggle")
                                    $("#" + source_id).modal("toggle")
                                })

                            })
                        }
                        $(".modal").on("shown.bs.modal", function (e) {
                            $("body").addClass("modal-open");
                        })
                        $(".modal").on("hidden.bs.modal", function (e) {
                            $("body").css("padding", "0px");
                        })
                        // bind click event to bookmark button
                        bindClick_bookmark()
                        // bind click event to record form
                        bindClick_record_form()
                        // bind click event to MLT button
                        bindClick_MLT_button()
                        // bind click event to remove tag
                        bindClick_tag_delete()
                    }).fail(function () {
                        alert('Failed to find more like this.')
                    });
                self.html('More Like This');
            }, 1000);
            // toggle collapse content
            $("#" + source_id + "_mlt_content").collapse('toggle')
        } else {
            // toggle collapse content
            $("#" + source_id + "_mlt_content").collapse('toggle')
        }
        return false;
    })
}
bindClick_MLT_button()

function addModal(record, record_id, doc_id) {

    let clone = $("#modal_template").clone(); // create copy 
    let desc = clone.find("[id^=mt]") // get all descendants w/ doc_id

    // first change all ids
    clone[0].id = record_id; // change id
    for (let i = 0; i < desc.length; i++) {
        let id = desc[i].id // get old id
        let parts = id.split("_")
        parts[0] = record_id // change record id
        new_id = parts.join("_") // create new id
        desc[i].id = new_id // update descendant id
    }

    // console.log(record)

    // next update modal content
    clone.attr('class', "modal fade")
    clone.find("#" + record_id + "_title").text(record.title) // title
    // record type
    let clr = (record.doc_type == "project") ? "primary-color-dark" : "deep purple darken-4"
    clone.find("#" + record_id + "_record_type").html(
        `<span class="badge ` + clr + ` text-capitalize z-depth-0 p-2">` +
        record.doc_type +
        `</span>`
    )

    // record tags
    if (record.tags) {
        for (let i = 0; i < record.tags.length; i++) {
            let tag = record.tags[i].split('_').join(' ')
            clone.find("#" + record_id + "_tags").append(
                `<h4 id="` + record_id + "_" + tag + "_tag" + `" class="d-inline">` +
                `<span class="badge teal darken-1 z-depth-0 p-2">` +
                tag +
                `<i class="close fa fa-times pt-0 pl-2 pr-0 text-white"
                        style="line-height:18px; font-size: 1.0rem; font-weight: lighter;"></i>` +
                `</h4>`
            )
        }
    }
    // record element tags
    if (record.element_tags) {
        for (let i = 0; i < record.element_tags.length; i++) {
            let tag = record.element_tags[i].split('_').join(' ')
            clone.find("#" + record_id + "_elem_tags").append(
                `<h4 id="` + record_id + "_" + tag + "_tag" + `" class="d-inline">` +
                `<span class="badge orange darken-4 z-depth-0 p-2">` +
                tag +
                `<i class="close fa fa-times pt-0 pl-2 pr-0 text-white"
                        style="line-height:18px; font-size: 1.0rem; font-weight: lighter;"></i>` +
                `</h4>`
            )
        }
    }
    clone.find("#" + record_id + "_abstract").text(record.abstract) // abstract
    // projects only
    if (record.doc_type == "project") {
        // status
        if (record.status) {
            var status = record.status
        } else {
            var status = "Not Specified"
        }
        clone.find("#" + record_id + "_status").html(
            `<h4 class="mb-2 mt-2">
                Status:
            </h4>
            <p class="m-0">` +
            status +
            `</p>`
        )
        // funding
        if (record.funding) {
            clone.find("#" + record_id + "_funding").html(
                `<h4 class="mb-2 mt-2">
                    Fund Amount:
                </h4>
                <p class="m-0">` +
                "$" + record.funding.toLocaleString({
                    style: 'currency',
                    currency: 'USD',
                    minimumFractionDigits: 2
                }) +
                `</p>`
            )
        }
        // funding agencies
        if (record.funding_agencies.length) {
            clone.find("#" + record_id + "_fundagencies").html(
                `<h4 class="mb-2 mt-2">
                        Funding Organizations:
                </h4>`
            )
            for (let i = 0; i < record.funding_agencies.length; i++) {
                clone.find("#" + record_id + "_fundagencies").append(
                    `<p class="m-0">` +
                    record.funding_agencies[i].name +
                    `</p>`
                )
            }
        }
        // performing agencies
        if (record.performing_agencies.length) {
            clone.find("#" + record_id + "_perfagencies").html(
                `<h4 class="mb-2 mt-2">
                        Perfroming Agencies:
                </h4>`
            )
            for (let i = 0; i < record.performing_agencies.length; i++) {
                clone.find("#" + record_id + "_perfagencies").append(
                    `<p class="m-0">` +
                    record.performing_agencies[i].name +
                    `</p>`
                )
            }
        }
        // managing agencies
        if (record.managing_agencies.length) {
            clone.find("#" + record_id + "_managencies").html(
                `<h4 class="mb-2 mt-2">
                        Managing Agencies:
                </h4>`
            )
            for (let i = 0; i < record.managing_agencies.length; i++) {
                clone.find("#" + record_id + "_managencies").append(
                    `<p class="m-0">` +
                    record.managing_agencies[i].name +
                    `</p>`
                )
            }
        }
        // start date
        if (!(record.start_date == null)) {
            clone.find("#" + record_id + "_startdate").text(record.start_date)
        }
        // completion date
        if (!(record.expected_complete_date == null) || !(record.actual_complete_date == null)) {
            let exp = !(record.expected_complete_date == null) ? record.expected_complete_date : "Not Specified"
            let act = !(record.actual_complete_date == null) ? record.actual_complete_date : "Not Specified"
            clone.find("#" + record_id + "_compdate").text(exp + " / " + act)
        }

    } else if (record.doc_type == "publication") {

        // authors
        if (record.authors.length) {
            clone.find("#" + record_id + "_authors").html(
                `<h4 class="mb-2 mt-2">
                    Authors:
                </h4>`
            )
            for (let i = 0; i < record.authors.length; i++) {
                let author = record.authors[i]
                clone.find("#" + record_id + "_authors").append(
                    `<p class="m-0">` +
                    author.lastname + ", " + author.firstname +
                    `</p>`
                )
            }
        }
        // publication date
        if (record.publication_date) {
            clone.find("#" + record_id + "_pubdate").html(
                `<h3 class="mb-2 mt-2">Publication Date: </h3>
                <p class="m-0">` +
                record.publication_date +
                `</p>`
            )
        }

    }

    // urls
    if (record.urls.length) {
        clone.find("#" + record_id + "_urls").html(
            `<h4 class="mb-2 mt-2">
                URLs:
            </h4>`
        )
        for (let i = 0; i < record.urls.length; i++) {
            let url = record.urls[i]
            clone.find("#" + record_id + "_urls").append(
                `<p class="ellipses w-50 m-0">
                    <a href=` + url + `>` + url + `</a>
                </p>`
            )
        }
    }

    // update record form
    clone.find("#" + record_id + "_objective1_label").attr('for', record_id + '_objective1')
    clone.find("#" + record_id + "_objective2_label").attr('for', record_id + '_objective2')
    clone.find("#" + record_id + "_objective3_label").attr('for', record_id + '_objective3')
    clone.find("#" + record_id + "_objective4_label").attr('for', record_id + '_objective4')
    if (record.objectives) {
        if (record.objectives.includes("objective1")) {
            clone.find("#" + record_id + '_objective1').attr('checked', true)
        }
        if (record.objectives.includes("objective2")) {
            clone.find("#" + record_id + '_objective2').attr('checked', true)
        }
        if (record.objectives.includes("objective3")) {
            clone.find("#" + record_id + '_objective3').attr('checked', true)
        }
        if (record.objectives.includes("objective4")) {
            clone.find("#" + record_id + '_objective4').attr('checked', true)
        }
    }
    if (record.notes) {
        clone.find("#" + record_id + "_notes").text(record.notes)
    }
    clone.find("#" + record_id + "_form").find("input[name='doc_id']").val(record_id)
    clone.find("#" + record_id + "_form").find("input[name='index']").val(record.doc_type + "s")
    clone.find("#" + record_id + "_form").find("input[name='type']").val(record.doc_type)

    // update bookmark button
    clone.find("#" + record_id + "_modal_bookmark_btn").val(record.doc_type + "s")
    if (record.bookmarked == "true") {
        // clone.find("#"+record_id+"_modal_bookmark_btn").toggleClass("unmarked")
        clone.find("#" + record_id + "_modal_bookmark_btn").toggleClass("marked")
        clone.find("#" + record_id + "_modal_bookmark_icon").attr('class', 'fa fa-bookmark fa-lg pr-1')
        clone.find("#" + record_id + "_modal_bookmark_text").text("Marked")
    }

    // update mlt button
    clone.find("#" + record_id + "_mlt_btn").attr('name', record.doc_type + "s")

    clone.appendTo("#modals") // append new modal

}

// bind click event to bookmark buttons
function bindClick_bookmark() {
    $("[id$=_bookmark_btn]").unbind("click") // first unbins all click events
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
}
bindClick_bookmark()

// bind click event to record form submit buttons
function bindClick_record_form() {
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
}
bindClick_record_form()


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