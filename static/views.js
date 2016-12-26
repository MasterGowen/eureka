var template_answer = `
    <tr>
        <td type_field='index'>1</td>
        <td type_field='price'>2</td>
        <td type_field='created'>3</td>
        <td type_field='url'>4</td>
        <td type_field='description'>5</td>
    </tr>`
function view_answers_bid_detail(obj){
    console.log(obj);
    return;
    var content_answers = $("#content_answers");
    for (var i = 0; i < 0; i++)
    {
        content_answers.append($(template_answer));
        $(content_answers.find("[type_field='index']").get(-1)).html("");
    }
}

/*[
    {
    "model": "core.answer", "pk": 2,
    "fields":
        {
        "author": 2,
        "bid": "04f1d39c-b8eb-42e5-ab77-41cc1e95c151",
        "description": "\u041a\u0440\u0430\u0441\u043d\u044b\u0439 \u0441 \u0431\u043e\u043b\u044c\u0448\u0438\u043c\u0438 \u0446\u044b\u0444\u0440\u0430\u043c\u0438",
        "status": 0,
        "price": "1550.00",
        "currency": "rur",
        "url": "http://avito.ru",
        "created": "2016-12-03T07:36:03",
        "updated": "2016-12-03T07:36:03"
        }
    },
    {
    "model": "core.answer",
    "pk": 3,
    "fields":
        {
        "author": 2,
        "bid": "04f1d39c-b8eb-42e5-ab77-41cc1e95c151",
        "description": "\u041c\u043e\u0442\u043e\u0440\u043e\u043b\u0430 \u0441\u0430\u043c\u0430\u044f \u043f\u0440\u043e\u0441\u0442\u0430\u044f \u0438 \u043d\u0430\u0434\u0435\u0436\u043d\u0430\u044f",
        "status": 0,
        "price": "560.00",
        "currency": "rur",
        "url": "http://avito.ru",
        "created": "2016-12-03T07:36:44",
        "updated": "2016-12-03T07:36:44"
        }
    },

    "model": "core.answer", "pk": 4, "fields": {"author": 2, "bid": "04f1d39c-b8eb-42e5-ab77-41cc1e95c151", "description": "\u041e\u0440\u0435\u0445\u043e\u043a\u043e\u043b ))", "status": 0, "price": "10.00", "currency": "rur", "url": "http://avito.ru", "created": "2016-12-03T07:37:10", "updated": "2016-12-03T07:37:10"}}]*/