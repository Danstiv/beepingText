# Beeping Text
This addon adds the ability to replace serten strings in speech with beeps.

## Rationale

We have some application that displays logs withlong lines, each line begins with the date and time, and we just want to sit behind the terminal and listen to these logs.

Also we want to read a few log lines quickly without stopping the app.

The date at the beginning of each line does not allow to quickly read such logs, and the solution exists, we can cut it using the functionality of NVDA speech dictionaries.

However, we will no longer have the opportunity to understand whether there is a date in the text, or it was replaced.

Later, we can read some kind of text on the Internet, NVDA will meet the date in the same format as in the logs, and we can never know that it was cut out from speech.

This addon allows to replace the text with beep, and thus, the user will always know that some text has been replaced or cut.

## How to use
Simply add a new entry to the NVDA speech dictionary, but use special marker for replacement.

Currently the marker is: @replace_with_beep@

It can be made configurable in the future.

Addon will capture replacement marker, remove it from speech, and replace it with beep.

Actually your replacement should start from replacement marker, and you could build your rephrased version after it.

Consider the following example:

`time="2025-09-08T00:01:58.332159100+07:00" level=info msg="Start initial configuration in progress"`

We could use the following regex: `time="\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d.\d{9}\+\d\d:\d\d" `

And replace with replacement marker.

As the result will receive the following text: `level=info msg="Start initial configuration in progress"`

But we also could use more advanced replacement technique.

Regex: `time="\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d.\d{9}\+\d\d:\d\d" level=(info|warning|error) msg="(.*?)"`
Replacement: `@replace_with_beep@\1 \2`

Thus: we can use all the capabilities of speech dictionaries, while each replaced phrase will be marked by beep, which will not allow to miss an unexpected replacement.

## Available markers
- `@replace_with_beep@` - replace marker with short beep.
- `@lower_pitch@` - replace marker with change pitch command in the speech sequence, that lowers the speech pitch.
- `@restore_pitch@` - replace marker with change pitch command in the speech sequence, that restores speech pitch to normal.

## Examples
### Read emoji with lower pitch
Regex: `((?:[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|[\U00002600-\U000026FF]|[\U00002700-\U000027BF])+)`

Replacement: `@lower_pitch@\1@restore_pitch@`
