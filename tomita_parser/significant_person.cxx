#encoding "utf8"
#GRAMMAR_ROOT S

S -> Word*
     (Noun<kwtype="Должность"> interp(SignificantPerson.Position))
     Noun<kwtype="ПерсонаВолгограда"> interp(SignificantPerson.Name)
     Word*;