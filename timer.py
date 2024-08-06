def timer_thread(): #Механика изменения времени

    global end
    global game_started
    global end_bad

    global timer
    global vent_timer
    global right_door_timer
    global left_door_timer

    global left_door_statement
    global right_door_statement
    global ventilation_statement

    while True:
        if game_started:

            time.sleep(1)
            timer -= 1

            if timer == 0:

                end = True
                break

            #Открытие дверей и вентиляции если они слишком долго закрыты

            if right_door_timer > 0:
                if right_door_statement == False:
                        
                        right_door_timer -= 1

            else:

                right_door_statement = True

            if left_door_timer > 0:
                if left_door_statement == False:

                    left_door_timer -= 1
            
            else:

                left_door_statement = True

            
            if vent_timer > 0:
                if ventilation_statement == False:

                    vent_timer -= 1
            
            else:

                ventilation_statement = True

            #Проверяем закончилась ли игра
            if end == True or end_bad == True:
                #Если да то ждем 1 сек чтоб бот отдохнул и возвращаем таймер к старому значению и отключаем конец плохой конец на всякий случай и игра начата 
                time.sleep(1)
                timer = 630
                end = False
                end_bad = False
                game_started = False
        #На всякий случай чтобы код не ломался.
        else:
            pass
