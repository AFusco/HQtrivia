#!/bin/bash

# TEXT=$(tesseract $1 stdout -l eng --psm 1 | grep .)
alphabet="/\!%&/()=?^àèìòù@çabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890"
TEXT=$(tesseract $1 stdout -c tessedit_char_whitelist="$alphabet" -l eng --psm 1 2>/dev/null | grep . )

q=$(echo "$TEXT" | head -n -3 | tr '\n' ' ' )

a_1=$(echo "$TEXT" | tail -n 3 | head -1)
a_2=$(echo "$TEXT" | tail -n 2 | head -1)
a_3=$(echo "$TEXT" | tail -n 1)

echo "{"
echo "\"question\": \"$q\","
echo "\"a_1\": \"$a_1\","
echo "\"a_2\": \"$a_2\","
echo "\"a_3\": \"$a_3\""
echo "}"

