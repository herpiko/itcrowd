
// Token untuk XSS

$('#clear_button_act').click(function(){
    $('#testingtext').text('hapus');
});
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
             }
        }
        return cookieValue;
    }

    $('.dragbox').hover(
        function(){
            var idnyadragbox = $(this).attr('id');
            $('eye_' + idnyadragbox).show();
        }
    );

    // inisialisasi koordinat

            // kotaktodo
            todo_c_position=$("#todo").position();
            todo_c_top=todo_c_position.top;
            todo_c_left=todo_c_position.left;
            todo_c = "(" + todo_c_top + "." + todo_c_left + ")";
            // kotakdoing
            doing_c_position=$("#doing").position();
            doing_c_top=doing_c_position.top;
            doing_c_left=doing_c_position.left;
            doing_c = "(" + doing_c_top + "." + doing_c_left + ")";
            // kotakdone
            done_c_position=$("#done").position();
            done_c_top=done_c_position.top;
            done_c_left=done_c_position.left;
            done_c = "(" + done_c_top + "." + done_c_left + ")";



            // variable utama
            var penjarak = 60;
            var todo_count = 0;
            var doing_count = 0;
            var done_count = 0;
            var todo_c_tinggi = todo_c_top + penjarak;
            var doing_c_tinggi = doing_c_top + penjarak;
            var done_c_tinggi = done_c_top + penjarak;

		lebar = $('.dropbox').width();
		lebardragbox = (90/100)*lebar;
		margindropbox = (lebar-lebardragbox)/1.5;
        $(".dragbox").fadeIn('slow');
        lebar = $('.dropbox').width();
		lebardragbox = (100/100)*lebar;
		$('.dragbox').width(lebardragbox);


        var kanban_obj;
        $.ajax({url:"/main/gtd_get_json/", async:false, success:function(result){
                kanban_obj = result;
        }});

                // beri index key
                var jumlah_kartu = 0
                var index=[];
                for (var x in kanban_obj){
                     index.push(x);
                     jumlah_kartu += 1;
                }

                // urutin
                index.sort(function (a,b) {
                    return a == b ? 0 : ( a > b ? 1 : -1);
                });


        function urutkan_kartu(){
            // Urutin kartu dalam todo
            for (y in kanban_obj){
                if (kanban_obj[y].fields.slot == 'todo'){
                    idnya = kanban_obj[y].fields.noid_tin;
                    var tingginya = $('#' + idnya).height();
                    $('#' + idnya).animate({
                        top : todo_c_tinggi,
                        left : todo_c_left + margindropbox
                    });
                todo_c_tinggi = todo_c_tinggi + tingginya +20;
                todo_count = todo_count +1;
                $("#todo_coordinate").text(todo_count);
                }
                if ((todo_c_tinggi - todo_c_top - 5)<100){
                    $("#todo").height(300);
                } else {
                    $("#todo").height(todo_c_tinggi - todo_c_top - 5);
                }
            }
            // Urutin kartu dalam doing
            for (y in kanban_obj){
                if (kanban_obj[y].fields.slot == 'doing'){
                    idnya = kanban_obj[y].fields.noid_tin;
                    var tingginya = $('#' + idnya).height();
                    $('#' + idnya).animate({
                        top : doing_c_tinggi,
                        left : doing_c_left + margindropbox
                    });
                doing_c_tinggi = doing_c_tinggi + tingginya +20;
                doing_count = doing_count + 1;
                $("#doing_coordinate").text(doing_count);
                }
                if ((doing_c_tinggi - doing_c_top - 5)<100){
                    $("#doing").height(300);
                } else {
                    $("#doing").height(doing_c_tinggi - doing_c_top - 5);
                }
            }
            // Urutin kartu dalam done
            for (y in kanban_obj){
                if (kanban_obj[y].fields.slot == 'done'){
                    idnya = kanban_obj[y].fields.noid_tin;
                    var tingginya = $('#' + idnya).height();
                    $('#' + idnya).animate({
                        top : done_c_tinggi,
                        left : done_c_left + margindropbox
                    });
                done_c_tinggi = done_c_tinggi + tingginya +20;
                done_count = done_count + 1;
                $("#done_coordinate").text(done_count);
                }
                if ((done_c_tinggi - done_c_top - 5)<100){
                    $("#done").height(300);
                } else {
                    $("#done").height(done_c_tinggi - done_c_top - 5);
                }
            }
        }

        urutkan_kartu();
//    }); // document ready end

    function tersimpan(){
            $('#testingtext').text('Tersimpan...');
        $('#testingtext').slideDown(function(){
            setTimeout(function(){
                $('#testingtext').fadeOut(1000);},0)

            });
        }

    $(".dragbox").draggable({

            // fungsi yang berjalan ketika objek mulai diangkat

            start:function(evt,ui){
                $(this).classname = 'draggable flying';
                var searchresult;
                var searchkey = $(this).attr('id');
                for(var i = 0; i < jumlah_kartu; i += 1){
                    if( kanban_obj[index[i]].fields.noid_tin == searchkey){
                    kanban_obj[index[i]].fields.slot += '-flying';
                    searchresult = kanban_obj[index[i]].fields;
                    }
                }

                // pengurangan koordinat tinggi setiap objek diangkat
                if(searchresult.slot == 'todo-flying'){
                    todo_count = todo_count - 1;
                    todo_c_tinggi = todo_c_top + penjarak;
                    $("#todo_coordinate").text(todo_count);
            for (y in kanban_obj){
                if (kanban_obj[y].fields.slot == 'todo'){
                    idnya = kanban_obj[y].fields.noid_tin;
                    var tingginya = $('#' + idnya).height();
                    $('#' + idnya).animate({
                        top : todo_c_tinggi,
                        left : todo_c_left + margindropbox
                    });
                todo_c_tinggi = todo_c_tinggi + tingginya +20;
                $("#todo_coordinate").text(todo_count);
                $("#todo").height(todo_c_tinggi - todo_c_top - 5);
                }
            }
                }
                if(searchresult.slot == 'doing-flying'){
                    doing_count = doing_count - 1;
                    doing_c_tinggi = doing_c_top + penjarak;
                    $("#doing_coordinate").text(doing_count);
            for (y in kanban_obj){
                if (kanban_obj[y].fields.slot == 'doing'){
                    idnya = kanban_obj[y].fields.noid_tin;
                    var tingginya = $('#' + idnya).height();
                    $('#' + idnya).animate({
                        top : doing_c_tinggi,
                        left : doing_c_left + margindropbox
                    });
                doing_c_tinggi = doing_c_tinggi + tingginya +20;
                $("#doing_coordinate").text(doing_count);
                $("#doing").height(doing_c_tinggi - doing_c_top - 5);
                }
            }
                }
                if(searchresult.slot == 'done-flying'){
                    done_count = done_count - 1;
                    done_c_tinggi = done_c_top + penjarak;
                    $("#done_coordinate").text(done_count);
            for (y in kanban_obj){
                if (kanban_obj[y].fields.slot == 'done'){
                    idnya = kanban_obj[y].fields.noid_tin;
                    var tingginya = $('#' + idnya).height();
                    $('#' + idnya).animate({
                        top : done_c_tinggi,
                        left : done_c_left + margindropbox
                    });
                done_c_tinggi = done_c_tinggi + tingginya +20;
                $("#done_coordinate").text(done_count);
                $("#done").height(done_c_tinggi - done_c_top - 5);
                }
            }

                }

                },
                });

$(".dropbox").droppable({
		 tolerance: 'intersect',
		    drop: function(event, ui) {
		    	lebar = $('.dropbox').width();
				lebardragbox = (90/100)*lebar;
				margindropbox = (lebar-lebardragbox)/2;


		        var drop_p = $(this).offset();
		        var drag_p = ui.draggable.offset();
		        var left_end = drop_p.left - drag_p.left + margindropbox;
		        var top_end = drop_p.top - drag_p.top + margindropbox;

                if(ui.draggable.position().top > todo_c_top && (ui.draggable.position().left+(ui.draggable.width()/2)) > todo_c_left &&  (ui.draggable.position().left+(ui.draggable.width()/2)) < doing_c_left ){
                    tingginya = ui.draggable.height();
		            ui.draggable.animate({
            	        top: todo_c_tinggi,
		                left: todo_c_left+margindropbox
                    });
                    // cari objek untuk penetapan variabel slot yang baru
                    var searchresult;
                    var searchkey = ui.draggable.attr('id');
                    for(var i = 0; i < jumlah_kartu; i += 1){
                        kanban_obj[index[i]];
                        if(kanban_obj[index[i]].fields.noid_tin == searchkey){
                            kanban_obj[index[i]].fields.slot = 'todo';
                        }
                    }
                    todo_c_tinggi = todo_c_tinggi + tingginya +20;
                    todo_count = todo_count +1;
                    $("#todo_coordinate").text(todo_count);
                    $("#todo").height(todo_c_tinggi - todo_c_top - 5);
                    // Ajax update
                    $.ajax({
                        type: "GET",
                        url : "/main/gtd_post_kanban_update/?idnya=" + searchkey + "&slot=todo",
                        success : function(){
                            tersimpan();
                        }
                    });
                    $("#eye_" + searchkey).html("<span class='fui-gear'></span>");
                    }

                if(ui.draggable.position().top > doing_c_top && (ui.draggable.position().left+(ui.draggable.width()/2)) > doing_c_left &&  (ui.draggable.position().left+(ui.draggable.width()/2)) < done_c_left ){
                    tingginya = ui.draggable.height();
		            ui.draggable.animate({
            	        top: doing_c_tinggi,
		                left: doing_c_left+margindropbox
                    });
                    // cari objek untuk penetapan variabel slot yang baru
                    var searchresult;
                    var searchkey = ui.draggable.attr('id');
                    for(var i = 0; i < jumlah_kartu; i += 1){
                        kanban_obj[index[i]];
                        if(kanban_obj[index[i]].fields.noid_tin == searchkey){
                            kanban_obj[index[i]].fields.slot = 'doing';
                        }
                    }
                    doing_c_tinggi = doing_c_tinggi + tingginya +20;
                    doing_count = doing_count + 1;
                    $("#doing_coordinate").text(doing_count);
                    $("#doing").height(doing_c_tinggi - doing_c_top - 5);
                    // Ajax update
                    $.ajax({
                        type: "GET",
                        url : "/main/gtd_post_kanban_update/?idnya=" + searchkey + "&slot=doing",
                        success : function(){
                            tersimpan();
                        }
                        });

                    $("#eye_" + searchkey).html("<span class='fui-gear'></span>");
                    }

                if(ui.draggable.position().top > done_c_top && (ui.draggable.position().left+(ui.draggable.width()/2)) > done_c_left){
                    tingginya = ui.draggable.height();
		            ui.draggable.animate({
            	        top: done_c_tinggi,
		                left: done_c_left+margindropbox
                    });
                    // cari objek untuk penetapan variabel slot yang baru
                    var searchresult;
                    var searchkey = ui.draggable.attr('id');
                    for(var i = 0; i < jumlah_kartu; i += 1){
                        kanban_obj[index[i]];
                        if(kanban_obj[index[i]].fields.noid_tin == searchkey){
                            kanban_obj[index[i]].fields.slot = 'done';
                        }
                    }
                    done_c_tinggi = done_c_tinggi + tingginya +20;
                    done_count = done_count + 1;
                    $("#done_coordinate").text(done_count);
                    $("#done").height(done_c_tinggi - done_c_top - 5);
                    // Ajax update
                    $.ajax({
                        type: "GET",
                        url : "/main/gtd_post_kanban_update/?idnya=" + searchkey + "&slot=done",
                        success : function(){
                            tersimpan();
                            //setTimeout(function(){
                            //$("#" + searchkey).fadeOut("slow");
                            //}, 500);
                        }
                    });
                    $("#eye_" + searchkey).html("<span class='fui-check'></span>");

                    }
            }


	});

