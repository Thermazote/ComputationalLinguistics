#encoding "utf8"
#GRAMMAR_ROOT S

ProperName -> Word<h-reg1, gram="фам, муж"> interp(SignificantPerson.LastName) 
              Word<h-reg1, gram="имя, муж"> interp(SignificantPerson.FirstName) 
              Word<h-reg1, gram="отч, муж"> interp(SignificantPerson.Patronymic); 
              // Бочаров Андрей Иванович
 
ProperName -> Word<h-reg1, gram="фам, муж"> interp(SignificantPerson.LastName) 
              Word<h-reg1, gram="имя, муж"> interp(SignificantPerson.FirstName); 
              // Бочаров Андрей
 
ProperName -> Word<h-reg1, gram="фам, муж"> interp(SignificantPerson.LastName);
              // Бочаров

ProperName -> Word<h-reg1, gram="имя, муж"> interp(SignificantPerson.FirstName) 
              Word<h-reg1, gram="отч, муж"> interp(SignificantPerson.Patronymic); 
              // Андрей Иванович
 
ProperName -> Word<h-reg1, gram="имя, муж"> interp(SignificantPerson.FirstName) 
              Word<h-reg1, gram="фам, муж"> interp(SignificantPerson.LastName);  
              // Андрей Бочаров


// --------------------------------------------------------------------------------


ProperName -> Word<h-reg1, gram="фам, жен"> interp(SignificantPerson.LastName) 
              Word<h-reg1, gram="имя, жен"> interp(SignificantPerson.FirstName) 
              Word<h-reg1, gram="отч, жен"> interp(SignificantPerson.Patronymic); 
              // Голикова Татьяна Алексеевна
 
ProperName -> Word<h-reg1, gram="фам, жен"> interp(SignificantPerson.LastName) 
              Word<h-reg1, gram="имя, жен"> interp(SignificantPerson.FirstName); 
              // Голикова Татьяна
 
ProperName -> Word<h-reg1, gram="фам, жен"> interp(SignificantPerson.LastName);
              // Голикова

ProperName -> Word<h-reg1, gram="имя, жен"> interp(SignificantPerson.FirstName) 
              Word<h-reg1, gram="отч, жен"> interp(SignificantPerson.Patronymic); 
              // Татьяна Алексеевна
 
ProperName -> Word<h-reg1, gram="имя, жен"> interp(SignificantPerson.FirstName) 
              Word<h-reg1, gram="фам, жен"> interp(SignificantPerson.LastName);
              // Татьяна Голикова

 
Person -> ProperName;
 
// Пример: "Выразил ясность по данному вопросу губернатор Волгоградской области Андрей Бочаров, упомянув, что необходимо двигаться дальше".
S -> Word* 
     Noun<kwtype="Должность", nc-agr[1]> interp(SignificantPerson.Position)
     Word*     
     Person<nc-agr[1], rt>
     Word*; 

// Пример: "Величественный губернатор призвал народ сохранять спокойствие".
S -> Word<nc-agr[1]>*
     Noun<kwtype="Должность", nc-agr[1]> interp(SignificantPerson.Position)
     Word<nc-agr[1]>*;
