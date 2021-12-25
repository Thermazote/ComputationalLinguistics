#encoding "utf-8"
#GRAMMAR_ROOT S  

// сад
AtrName -> 'музей' | 'зал' | 'собор' | 'филармония' | 
           'авангард' | 'библиотека' | 'площадь' | 'памятник' | 
           'церковь' | 'эшелон' | 'мельница' | 'гора' | 
           'элеватор' | 'фонтан' | 'курган' | 'опера' | 
           'порт' | 'парк' | 'сквер' | 'планетарий' | 
           'горсад' | 'арена' | 'бармалей';

// InterpAtr -> AtrName interp(Attraction.Name);

Adj_AtrName -> (Word<nc-agr[1], gram="sg">) Adj<nc-agr[1]>* AtrName<nc-agr[1], rt> |
               AtrName<nc-agr[1], rt> Adj<nc-agr[1]> Noun<nc-agr[1]>;

AtrName_Noun -> AtrName<nc-agr[1], rt> Noun<nc-agr[1]> |
                AtrName<rt> Word<gram="gen"> | 
                AtrName<rt> Noun |
                Noun<nc-agr[1]> AtrName<nc-agr[1], rt> Adj<nc-agr[1]> Noun<nc-agr[1]>;

AtrName_Person -> AtrName<nc-agr[1], rt> (Noun<nc-agr[1]>) Word<nc-agr[1], gram="имя"> Word<nc-agr[1], gram="фам"> |
                  AtrName<nc-agr[1], rt> (Noun<nc-agr[1]>) Word<nc-agr[1], gram="фам"> |
                  AtrName<nc-agr[1]> Word<nc-agr[1], gram="persn"> | 
                  Adj<nc-agr[1]> AtrName<nc-agr[1], rt> Adj<nc-agr[1]> Word<nc-agr[1], gram="persn">;

Geo_AtrName -> Word<nc-agr[1], gram="geo"> AtrName<nc-agr[1], rt> |
               AtrName<nc-agr[1], rt> Noun<nc-agr[1]> Adj<nc-agr[2], gram="geo"> Noun<nc-agr[2]>;

S -> Adj_AtrName interp(Attraction.Name) | AtrName_Noun interp(Attraction.Name) | AtrName_Person interp(Attraction.Name) | 
    Geo_AtrName interp(Attraction.Name) | AtrName interp(Attraction.Name);
































// S -> Word*
//      Noun<kwtype="ДостопримечательностьВолгограда"> interp(Attraction.Name)
//      Word*;

// SightType -> 'музей' | 'зал' | 'собор' | 'авангард' | 'библиотека' | 'площадь' | 'памятник' | 'церковь' | 'эшелон' | 'дом павлова' | 'мельница гергардта';

// SightType -> Noun<kwtype="ДостопримечательностьВолгограда">;

// SightType -> 'музей' | 'ботанический сад';

// SightName -> DevotedEvent | DevotedPerson;

// DevotedEvent -> (Adj<gnc-agr[1]>) Noun<gnc-agr[1], rt> (Adj<gram="род">) (Noun<gram="род">);
// DevotedPerson -> Noun<h-reg1> Word<h-reg1>* | Noun Word<h-reg1>* | Word<h-reg1, gram="дат">;

// // AdjName -> Adj<~fw, h-reg1> Adj*;

// TypeFirst -> SightType interp(Attraction.Type) SightName interp(Attraction.Name);
// TypeLast -> SightName interp(Attraction.Name) SightType interp(Attraction.Type);

// Main -> TypeFirst | TypeLast;
