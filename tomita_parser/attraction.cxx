#encoding "utf-8"
#GRAMMAR_ROOT S     

S -> Word*
     Noun<kwtype="ДостопримечательностьВолгограда"> interp(Attraction.Name)
     Word*;


