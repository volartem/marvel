openerp.marvelapi = function (instance, local) {
    var _t = instance.web._t;
    var lt = instance.web._lt;
    var QWeb = instance.web.qweb;

    local.RequestApi = instance.Widget.extend({
        objects: [1, 2, 3],
        events: {
            'click #server-request': function () {
                console.log('server____request');
                $("#tables-body").empty();
                var data = this.$el.find("input#text").val();
                $.ajax({
                    url: "/comics/api",
                    async: false,
                    method: 'GET',
                    data: {text: data},
                    success: function (response) {
                        var result = $.parseJSON(response);
                        console.log(result);
                        // var tr_row = $("<tr />");
                        // $('#tables-body').append(tr_row);
                        $.each(result, function (i, item) {
                            var thumbnail = $('<img class="img-rounded"/>');
                            thumbnail.attr('src', item.thumbnail.path + "." + item.thumbnail.extension);
                            thumbnail.attr('alt', "No image found");
                            thumbnail.attr('height', 50);
                            var tr_row = $("<tr/>");
                            var entry_div = spoilerCreate(item);
                            tr_row.attr('class', 'spoiler-trigger collapsed');
                            tr_row.attr('data-toggle', 'collapse');
                            tr_row.attr('data-target', 'spoiler' + item.id);
                            tr_row.append($('<td/>').html(item.title))
                                .append($('<td/>').html(item.format))
                                .append($('<td/>').html(item.dates[0].date.slice(0, 10)))
                                .append($('<td/>').html(item.ean))
                                .append($('<td/>').html(thumbnail[0].outerHTML));

                            $('#tables-body').append(tr_row);
                            $('#tables-body').append(entry_div);
                            tr_row.bind('click', {info: item}, fullInfo);
                        });

                    }
                });
                this.objects = [1, 2, 3, 4, 5];
                console.log(this.objects);
            }
        },

        start: function () {
            console.log('local.requestapi__');
            return this.$el.append(QWeb.render("template_ajax", {objects: this.objects}));
        }
    });
    instance.web.client_actions.add(
        'marvelapi.requestapi', 'instance.marvelapi.RequestApi');
};
fullInfo = function (event) {
    var current_div = $(this).next();
    current_div.collapse('toggle');
};

//create hided div for spoiler
spoilerCreate = function (item) {
    var obj = $('<div/>');
    obj.append($('<p/>').html('Name: ' + item.title));
    obj.append($('<p/>').html('Description: ' + item.description));
    obj.append($('<p/>').html('Date: ' + item.dates[0].date.slice(0, 10)));
    obj.append($('<p/>').html('Characters: ' + iterate(item.characters.items)));
    obj.append($('<p/>').html('Stories: ' + iterate(item.stories.items)));
    obj.append(iterateImg(item.images));
    obj.append($('<p/>').append($('<button>Save</button>')
        .attr('id', 'id' + item.id))
        .click(
            {comic: item},
            saveComics
        ));
    return obj.attr('class', 'collapse').attr('id', 'spoiler' + item.id);
};
// function that iterate for list of objects and concatenate 'name' value
function iterate(list) {
    var output = '';
    $.each(list, function (index, value) {
        output += value['name'];
        output += ', ';
    });
    return output
}

// function that iterate for list of image objects and return "p" with images
function iterateImg(list) {
    var blockImages = $('<p/>');
    $.each(list, function (index, value) {
        var images = $('<img class="img-rounded"/>');
        images.attr('src', value.path + "." + value.extension);
        images.attr('height', 200);
        blockImages.append(images);
    });
    return blockImages
}
//save comics on db
saveComics = function (event) {
    console.log('save comics', event.data.comic);
    console.log('save comics', event);
    $.ajax({
        url: '/comics/api/save',
        method: 'POST',

        data: {
            comic: JSON.stringify(event.data.comic)
            //description: event.data.comic.description
        },
        success: function (response) {
            console.log('response__from__save', response);
        }
    })
};