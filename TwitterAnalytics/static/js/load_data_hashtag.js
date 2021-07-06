$(document).ready(function() {
    var title = $(this).attr('title')
    var hashtag = title.substring(0, title.search('-') - 1).toLowerCase()
    language = document.documentElement.lang

    //Important tweets of hashtag
    $.ajax({    
        url: '/load_important_tweets_hashtag/',
        type: 'GET',
        data: {"hashtag": hashtag, "lang": language},
        dataType: 'json',
    
        success : function(json) {
            data = JSON.parse(json)
            data.forEach(tweet => {
                let url_image = tweet['profile_image_url_https']
                let exists_image = tweet['check_url_image']
                let name = tweet['name']
                let nick = tweet['screen_name']
                let text = tweet['full_text']
                let date = tweet['created_at']
                let operating_system = tweet['source']
                let media = tweet['media']

                if(media) {
                    let media_url = tweet['media_url']
                    let media_type = tweet['media_type']
                    inner_tweet_with_media(url_image, exists_image, name, nick, text, date,operating_system, media_url, media_type)
                }
                else {
                    inner_tweet(url_image, exists_image, name, nick, text, date,operating_system)
                }
            });
        },
    
        error : function(xhr, status) {
            console.error('Disculpe, existió un problema al cargar los tweets importantes de ' + hashtag);
        },
    })

    //Important users of hashtag
    $.ajax({    
        url: '/load_important_users_hashtag/',
        type: 'GET',
        data: {"hashtag": hashtag, "lang": language},
        dataType: 'json',
    
        success : function(json) {
            data = JSON.parse(json)
            data.forEach(user => {
                let name = user['name']
                let screen_name = user['screen_name']
                let verified = user['verified']
                let description = user['description']
                let exists_image = user['check_url_image']
                let url_image = user['profile_image_url_https']
                let followers_count = user['followers_count']
        
                inner_important_user(name, screen_name, verified, description, exists_image, url_image, followers_count)
            });
        },
    
        error : function(xhr, status) {
            console.error('Disculpe, existió un problema al cargar los usuarios importantes importantes de ' + hashtag);
        },
    })

    //Activity tweets of hashtag
    $.ajax({    
        url: '/load_activity_tweets_hashtag/',
        type: 'GET',
        data: {"hashtag": hashtag, "lang": language},
        dataType: 'json',
    
        success : function(json) {
            data = JSON.parse(json)

            let id_days = '#chart-activity-tweets-per-days'
            var label = language === 'en' ? 'Display by days' : 'Visualización por días'

            chart_activity_tweets(id_days, data[0], label)

            let id_hours = '#chart-activity-tweets-per-hours'
            label = language === 'en' ? 'Display by hours' : 'Visualización por horas'

            chart_activity_tweets(id_hours, data[1], label)

            $("#hours-tweets").removeClass('visible')
          
        },
    
        error : function(xhr, status) {
            console.error('Disculpe, existió un problema al cargar la actividad de los tweets de ' + hashtag);
        },
    })

    //Activity users of hashtag
    data_chart_activity_users = []
    $.ajax({
        url: '/load_activity_users_hashtag/',
        type: 'GET',
        data: {"hashtag": hashtag, "lang": language},
        dataType: 'json',
    
        success : function(json) {
            data = JSON.parse(json)

            var id = 0
            data.forEach(user =>{
                data_chart = user[0]
                user = user[1]
                let name = user['name']
                let screen_name = user['screen_name']
                let verified = user['verified']
                let description = user['description']
                let exists_image = user['check_url_image']
                let url_image = user['profile_image_url_https']
                let followers_count = user['followers_count']
                data_chart_activity_users.push(data_chart)
                
                inner_activity_user(name, screen_name, verified, id, description, exists_image, url_image, followers_count)
                id++
            })
    
            //print first activity user
            var label = language === 'en' ? 'Display by days' : 'Visualización por días'
            chart_activity_days_tweets_users(data_chart_activity_users[0][0], data[0][1]['name'], label)
            
            var label = language === 'en' ? 'Display by hours' : 'Visualización por horas'
            chart_activity_hours_tweets_users(data_chart_activity_users[0][1], data[0][1]['name'], label)

            //$("#hours-users").removeClass('visible')
    
            $(".activity-user").on("click", function(a){
                childSelector = $(a.currentTarget).html()
                aux = childSelector.search("id=")
                id_user = parseInt(childSelector[aux + 4])
                title = childSelector.substring(childSelector.search("<p>") + 3, childSelector.search("</p>"))

                update_chart_activity_days_tweets_users(data_chart_activity_users[id_user][0], title)
                update_chart_activity_hours_tweets_users(data_chart_activity_users[id_user][1], title)
            });
        },
    
        error : function(xhr, status) {
            console.error('Disculpe, existió un problema al cargar la actividad de los usuarios de ' + hashtag);
        },
    })
});