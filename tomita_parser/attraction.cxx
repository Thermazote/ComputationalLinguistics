#encoding "utf-8"
#GRAMMAR_ROOT S     

S -> Word*
     Noun<kwtype="ТипПостройки"> interp(Attraction.BuildingType)
     Word*;


