def timing_thread(): #Механика передвижения роботов

    global timer, go_cleaner, go_hoverboard, go_crazy, go_barmen, night, game_started, go_terminator

    while True:

        if game_started: #Проверяем, началась ли игра

            if night == 1:  #Ночь 1 (Уборщик)
                go_barmen = False
                go_crazy = False
                go_hoverboard = False
                if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли уборщик или нет(шанс очень маленький)

                    time.sleep(5)
                    a = randint(1, 100)

                    if a == 50:

                        go_cleaner = True
                        print(go_cleaner)

                    else: 

                        print(timer)

                elif timer <= 540 and timer > 450: #Рандом пойдет ли уборщик в час ночи.

                    time.sleep(5)
                    a = randint(1, 5)

                    if a == 2 or a == 3:

                        go_cleaner = True
                        print(go_cleaner)

                    else:

                        print('z')
                        time.sleep(5)
                        go_cleaner = False
                        print(timer)

                elif timer <= 450 and timer > 360: #Рандом пойдет ли уборщик в 2 ночи.
                    
                    time.sleep(5)
                    a = randint(1, 5)

                    if a == 2 or 3:

                        go_cleaner = True

                    else:

                        time.sleep(5)
                        a = randint(1,4)

                        if a == 2 or a == 3:

                            go_cleaner == True
                            print(go_cleaner)

                        else:

                            print('i')
                            go_cleaner = False
                            print(timer)

                elif timer <= 360 and timer > 80: #Рандом пойдет ли уборщик в 3, 4, 5 ночи.

                    time.sleep(5)
                    a = randint(1, 5)

                    if a == 2 or a == 3:

                        go_cleaner = True
                        print(go_cleaner)

                    else:

                        print('f')
                        time.sleep(5)
                        go_cleaner = False
                        print(timer)

                elif timer <= 80: #Рандом пойдет ли уборщик в 6 ночи.

                    time.sleep(5)
                    a = randint(1, 4)

                    if a == 2 or a == 3 or a == 4:

                        go_cleaner = True

                    else:

                        print('m')
                        time.sleep(5)
                        go_cleaner = False
                        print(timer)


            elif night == 2: #Ночь 2 (Псих)
                    go_barmen = False
                    go_cleaner = False
                    go_hoverboard = False
                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли псих или нет(шанс очень маленький)
                        
                        time.sleep(3)
                        a = randint(1, 100)
                        
                        if a == 50:
                            
                            go_crazy = True
                            print(go_crazy)

                        else: 

                            print(timer)

                    elif timer <= 540 and timer > 450: #Рандом пойдет ли псих в час ночи.
                        
                        time.sleep(3)
                        a = randint(1, 5)
                        
                        if a == 2 or a == 3:
                            
                            go_crazy = True
                            print(go_crazy)

                        else:
                            
                            print('z')
                            time.sleep(3)
                            go_crazy = False
                            print(timer)

                    elif timer <= 450 and timer > 360: #Рандом пойдет ли уборщик в 2 ночи.

                        time.sleep(3)
                        a = randint(1, 5)

                        if a == 2 or 3:

                            go_crazy = True

                        else:

                            time.sleep(3)
                            a = randint(1,4)

                            if a == 2 or a == 3:

                                go_crazy == True
                                print(go_crazy)

                            else:

                                print('i')
                                go_crazy = False
                                print(timer)

                    elif timer <= 360 and timer > 80: #Рандом пойдет ли уборщик в 3, 4, 5 ночи.

                        time.sleep(3)
                        a = randint(1, 5)

                        if a == 2 or a == 3:

                            go_crazy = True
                            print(go_crazy)

                        else:

                            print('f')
                            time.sleep(3)
                            go_crazy = False
                            print(timer)

                    elif timer <= 80:

                        time.sleep(3)
                        a = randint(1, 4)

                        if a == 2 or a == 3 or a == 4: #Рандом пойдет ли уборщик в 6 ночи.

                            go_crazy = True

                        else:

                            print('m')
                            time.sleep(3)
                            go_crazy = False
                            print(timer)


            elif night == 3: #Ночь 3 (Бармен)
                    go_crazy = False
                    go_cleaner = False
                    go_hoverboard = False
                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли бармен или нет(шанс очень маленький)
                        
                        time.sleep(5)
                        a = randint(1, 100)
                        
                        if a == 50:
                            
                            go_barmen = True
                            print(go_barmen)

                        else: 

                            print(timer)

                    elif timer <= 540 and timer > 450: #Рандом пойдет ли бармен в час ночи.
                        
                        time.sleep(5)
                        a = randint(1, 5)
                        
                        if a == 2 or a == 3:
                            
                            go_barmen = True
                            print(go_barmen)

                        else:
                            
                            print('z')
                            time.sleep(5)
                            go_barmen = False
                            print(timer)

                    elif timer <= 450 and timer > 360: #Рандом пойдет ли бармен в 2 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or 3:

                            go_barmen = True

                        else:

                            time.sleep(5)
                            a = randint(1, 4)

                            if a == 2 or a == 3:

                                go_barmen == True
                                print(go_barmen)

                            else:

                                print('i')
                                go_barmen = False
                                print(timer)

                    elif timer <= 360 and timer > 80: #Рандом пойдет ли бармен в 3, 4, 5 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or a == 3:

                            go_barmen = True
                            print(go_barmen)

                        else:

                            print('f')
                            time.sleep(5)
                            go_barmen = False
                            print(timer)

                    elif timer <= 80:

                        time.sleep(5)
                        a = randint(1, 4)

                        if a == 2 or a == 3 or a == 4: #Рандом пойдет ли бармен в 6 ночи.

                            go_barmen = True

                        else:

                            print('m')
                            time.sleep(5)
                            go_barmen = False
                            print(timer)


            elif night  == 4: #Ночь 4 (Ховерборд)
                    
                    go_crazy = False
                    go_cleaner = False
                    go_barmen = False

                    if timer >= 541: #Рандом до 1 часа ночи(в игре) пойдет ли ховерборд или нет(шанс очень маленький)
                            
                            time.sleep(5)
                            a = randint(1, 100)
                            
                            if a == 50:
                                
                                go_hoverboard = True
                                print(go_hoverboard) #Нужно для тестирования

                            else: 

                                print(timer) #Нужно для тестирования

                    elif timer <= 540 and timer > 450: #Рандом пойдет ли бармен в час ночи.
                        
                        time.sleep(5)
                        a = randint(1, 5)
                        
                        if a == 2 or a == 3:
                            
                            go_hoverboard = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:
                            
                            print('z') #Нужно для тестирования
                            time.sleep(5)
                            go_hoverboard = False
                            print(timer) #Нужно для тестирования

                    elif timer <= 450 and timer > 360: #Рандом пойдет ли бармен в 2 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or 3:

                            go_hoverboard = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:

                            time.sleep(5)
                            a = randint(1,4)

                            if a == 2 or a == 3:

                                go_hoverboard == True
                                print(go_hoverboard) #Нужно для тестирования

                            else:

                                print('i')
                                go_hoverboard = False
                                print(timer) #Нужно для тестирования

                    elif timer <= 360 and timer > 80: #Рандом пойдет ли бармен в 3, 4, 5 ночи.

                        time.sleep(5)
                        a = randint(1, 5)

                        if a == 2 or a == 3:

                            go_barmen = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:

                            print('f') #Нужно для тестирования
                            time.sleep(5)
                            go_hoverboard = False
                            print(timer) #Нужно для тестирования

                    elif timer <= 80:

                        time.sleep(5)
                        a = randint(1, 4)

                        if a == 2 or a == 3 or a == 4: #Рандом пойдет ли ховерборд в 6 ночи.

                            go_hoverboard = True
                            print(go_hoverboard) #Нужно для тестирования

                        else:

                            print('m') #Нужно для тестирования
                            time.sleep(5)
                            go_hoverboard = False
                            print(timer) #Нужно для тестирования
                    elif night == 5: #Ночь 5 (Терминатор)
                        go_crazy = False
                        go_cleaner = False
                        go_barmen = False
                        go_terminator = False
                        if timer >= 541: 
                                
                                time.sleep(5)
                                a = randint(1, 100)
                                
                                if a == 50:
                                    
                                    go_terminator = True
                                    print(go_terminator) #Нужно для тестирования

                                else: 

                                    print(timer) #Нужно для тестирования

                        elif timer <= 540 and timer > 450:  
                            
                            time.sleep(5)
                            a = randint(1, 5)
                            
                            if a == 2 or a == 3:
                                
                                go_terminator = True
                                print(go_terminator) #Нужно для тестирования

                            else:
                                
                                print('z') #Нужно для тестирования
                                time.sleep(5)
                                go_terminator = False
                                print(timer) #Нужно для тестирования

                        elif timer <= 450 and timer > 360: 

                            time.sleep(5)
                            a = randint(1, 5)

                            if a == 2 or 3:

                                go_terminator = True
                                print(go_terminator) #Нужно для тестирования

                            else:

                                time.sleep(5)
                                a = randint(1,4)

                                if a == 2 or a == 3:

                                    go_terminator == True
                                    print(go_terminator) #Нужно для тестирования

                                else:

                                    print('i')
                                    go_terminator = False
                                    print(timer) #Нужно для тестирования

                        elif timer <= 360 and timer > 80: #Рандом пойдет ли терминатор в 3, 4, 5 ночи.

                            time.sleep(5)
                            a = randint(1, 5)

                            if a == 2 or a == 3:

                                go_terminator = True
                                print(go_terminator) #Нужно для тестирования

                            else:

                                print('f') #Нужно для тестирования
                                time.sleep(5)
                                go_terminator = False
                                print(timer) #Нужно для тестирования

                        elif timer <= 80:

                            time.sleep(5)
                            a = randint(1, 4)

                            if a == 2 or a == 3 or a == 4: #Рандом пойдет ли терминатор в 6 ночи.

                                go_terminator = True
                                print(go_terminator) #Нужно для тестирования

                            else:

                                print('m') #Нужно для тестирования
                                time.sleep(5)
                                go_terminator = False
                                print(timer) #Нужно для тестирования

        else:
            pass
