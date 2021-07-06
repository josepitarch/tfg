language = document.documentElement.lang

//Print pie chart of important hashtags
function chart_hashtags(data) {
    var ctx = $('#chart-hashtags')
    var myChart = new Chart(ctx, {
    type: 'pie',
        data: {
        labels: data[0],
        datasets: [{
        label: "Population (millions)",
        backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850", "#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"],
        data: data[1]
        }]
    },
    options: {
        title: {
        display: false,
        text: 'Pie chart hashtags del momento',
        },
        responsive: true,
        maintainAspectRatio: false,
    }
    });

    $("#chart-hashtags").click(function(evt) {
        var firstPoint = myChart.getElementAtEvent(evt)[0];
        
        if (firstPoint) {
            var label = myChart.data.labels[firstPoint._index];
            var value = myChart.data.datasets[firstPoint._datasetIndex].data[firstPoint._index];
            $("#input-hashtag").val(label + '/' + value)
            $("form#form-hashtag").submit()
        }
    })
}

//Print bar chart of tweets activity
function chart_activity_tweets(id, data, label) {
    var ctx = $(id)
    var activity_tweets = new Chart(ctx, {
    type: 'line',
        data: {
            labels: data[0],
            datasets: [{
            label: label,
            fill: true,
            backgroundColor: ['blue'],
            borderColor: ['black'],
            color: ['white'],
            data: data[1]
            }]
        },
    options: {
        title: {
        display: false,
        text: 'Bar chart actividad de los tweets',
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    min: 0
                }
            }]
        },
    }
    });
}

//Print bar chart of days tweets activity user
var activity_days_tweets_users;
function chart_activity_days_tweets_users(data, title, label) {
    var ctx = $('#chart-activity-users-per-days')
    activity_days_tweets_users = new Chart(ctx, {
    type: 'line',
    data: {
        labels: data[0],
        datasets: [{
        label: label,
        fill: true,
        backgroundColor: ['blue'],
        borderColor: ['black'],
        color: ['white'],
        data: data[1]
        }]
    },
    options: {
        title: {
        display: true,
        text: title,
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    min: 0
                }
            }]
        },
    }
    });
}

//Print bar chart of hours tweets activity user
var activity_hours_tweets_users;
function chart_activity_hours_tweets_users(data, title, label) {
    var ctx = $('#chart-activity-users-per-hours')
    activity_hours_tweets_users = new Chart(ctx, {
    type: 'line',
        data: {
            labels: data[0],
            datasets: [{
            label: label,
            backgroundColor: ['blue'],
            borderColor: ['black'],
            color: ['white'],
            data: data[1]
            }]
        },
    options: {
        title: {
        display: true,
        text: title,
        },
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            yAxes: [{
                display: true,
                ticks: {
                    beginAtZero: true,
                    min: 0
                }
            }]
        },
    }
    });
}

function update_chart_activity_days_tweets_users(data, title) {
    activity_days_tweets_users.data.labels = data[0]
    activity_days_tweets_users.data.datasets[0].data = data[1]
    activity_days_tweets_users.options.title.text = title

    activity_days_tweets_users.update();
}

function update_chart_activity_hours_tweets_users(data, title) {
    activity_hours_tweets_users.data.labels = data[0]
    activity_hours_tweets_users.data.datasets[0].data = data[1]
    activity_hours_tweets_users.options.title.text = title
 
    activity_hours_tweets_users.update();
}

function inner_tweet(url_image, exists_image, name, nick, text, date,operating_system) {
    let src = exists_image ? url_image : "../static/icons/usuario.png"
    
    $("#tweets-of-moment").append("<div class='media mb-3'><img src='" + src + "' class='img-fluid rounded-circle mr-3' alt='Imagen del perfil de usuario de Twitter'>"
    + "<div class='media-body'><p class='media-titulo'>" + name + "</p><p class='media-subtitulo'>@" + nick + "</p>"
    + "<p class='media-date text-muted text-right pr-3'>" + date + "</p><div><p class='media-text'>" + text 
    + "</p></div><p class='text-right text-muted media-operating-system'>" + operating_system + "</p></div>")
}

function inner_tweet_with_media(url_image, exists_image, name, nick, text, date,operating_system, media_url, media_type) {
    let src = exists_image ? url_image : "../static/icons/usuario.png"
    if(media_type == 'photo') {
        $("#tweets-of-moment").append("<div class='media mb-3'><img src='" + src + "' class='img-fluid rounded-circle mr-3' alt='Imagen del perfil de usuario de Twitter'>"
        + "<div class='media-body'><p class='media-titulo'>" + name + "</p><p class='media-subtitulo'>@" + nick + "</p>"
        + "<p class='media-date text-muted text-right pr-3'>" + date + "</p><div><p class='media-text'>" + text + 
        "</p><img class='img-fluid rounded' src='" + media_url + "'></div><p class='text-right text-muted mt-3 media-operating-system'>" 
        + operating_system + "</p></div></div></div>")
    }
    if(media_type == 'video') {
        $("#tweets-of-moment").append("<div class='media mb-3'><img src='" + src + "' class='img-fluid rounded-circle mr-3' alt='Imagen'>"
        + "<div class='media-body'><p class='media-titulo'>" + name + "</p><p class='media-subtitulo'>@" + nick + "</p>"
        + "<p class='media-date text-muted text-right pr-3'>" + date + "</p><div><p class='media-text'>" + text 
        + "</p><div class='embed-responsive embed-responsive-16by9'><iframe class='embed-responsive-item' "
        + "src='" + media_url + "' allowfullscreen></iframe></div></div><p class='text-right text-muted mt-3 media-operating-system'>" 
        + operating_system + "</p></div></div>")
    }
}

function inner_important_user(name, screen_name, verified, description, exists_image, url_image, followers_count) {
    let src = exists_image ? url_image : "../static/icons/usuario.png"
    let src_verified = "../static/icons/verified.png";
    let followers = language === 'en' ? " followers" : " seguidores"
    
    if(verified) {
        $(".list-important-users").append("<div class='col-12 col-md-5 d-flex flex-row my-2'><img src='" + src + "' class='img-fluid rounded-circle profile mr-3' alt='Imagen del perfil de usuario de Twitter'>" + 
        "<p>" + name + "</p><img src='" + src_verified + "' class='img-fluid rounded-circle verified mr-3' alt='Imagen verificación usuario Twitter'>"
        +  "<div class=' text-muted followers'>" + followers_count + followers +  "</div></div>")
    }
    else {
        $(".list-important-users").append("<div class='col-12 col-md-5 d-flex flex-row my-2'><img src='" + src + "' class='img-fluid rounded-circle profile mr-3' alt='Imagen del perfil de usuario de Twitter'>" + 
        "<p>" + name + "</p><div class='text-muted followers'>" + followers_count + followers +  "</div></div>")
    }
}

function inner_activity_user(name, screen_name, verified, id, description, exists_image, url_image, followers_count) {
    let src = exists_image ? url_image : "../static/icons/usuario.png"
    let src_verified = "../static/icons/verified.png";
    let followers = language === 'en' ? " followers" : " seguidores"
    
    if(verified) {
        $(".list-activity-users").append("<div class='col-12 activity-user d-flex flex-row my-2'><div class='d-flex flex-row' id='" + id + "'><img src='" + src + "' class='img-fluid rounded-circle profile mr-3' alt='Imagen del perfil de usuario de Twitter'>" + 
        "<p>" + name + "</p><img src='" + src_verified + "' class='img-fluid rounded-circle verified mr-3' alt='Imagen verificación usuario Twitter'>"
        +  "<div class=' text-muted followers'>" + followers_count + followers +  "</div></div></div>")
    }
    else {
        $(".list-activity-users").append("<div class='col-12 activity-user d-flex flex-row my-2'><div class='d-flex flex-row' id='" + id + "'><img src='" + src + "' class='img-fluid rounded-circle profile mr-3' alt='Imagen del perfil de usuario de Twitter'>" + 
        "<p>" + name + "</p><div class='text-muted followers'>" + followers_count + followers + "</div></div></div>")
    }
}