import urllib.request
import sys
import eyed3


# Program that automates id3 tag writing to .mp3 files.
# The programs assumes that all the .mp3 files are initialized with their publishing years.
# sy.argv[0] contains the wikipedia link to the album of the songs in the .mp3 files.
# sys.argv[1] may contain the path to the rules for the general tags (see documentation assign_gen_tags).
# Author: Mathijs Hubrechtsen

# -------------------------------------------------- Part: Substring Methods

# Get all the substrings in a given string located between the first case of a given start_target (exclusive)
# and end_target (exclusive). For example if this method is called on the following string:
#           string = text + start_target + substring + end_target + text
# This method will return substring.
def get_substrings_between(string, start_target, end_target):
    start = string.find(start_target)
    if start == -1:
        raise LookupError
    new_string = string[start + len(start_target): len(string)]
    end = new_string.find(end_target)
    if end == -1:
        raise LookupError
    return string[start + len(start_target): start + len(start_target) + end]


# Get all the substrings in a given string located between all the cases of a given start_target (exclusive)
# and end_target (exclusive). For example if this method is called on the following string:
#           string = text + start_target + substring_1 + end_target + text +
#                    start_target + substring_2 + end_target + text
# This method will return substring_1 and substring_2.
#
# NOTE: This specific implementation skips the first end_target after finding a start_target.
# For example if this implementation is called on the following string:
#           string = text + start_target + substring_1 + end_target + substring_2 + end_target + text
# This implementation will return substring_1 + end_target + substring_2
# This is done because of wikipedia's html layout.
def get_all_substrings_between(string, start_target, end_target):
    result = list()
    # As long as the start_target can be found do...
    start = string.find(start_target)
    while start != -1:
        # Move the string up.
        string = string[start + len(start_target): len(string)]

        # Correct for the second case of end_target, this is done bcs of wikipedia's html layout.
        # Find the first case:
        end1 = string.find(end_target)
        # Find the second case:
        end2 = string[end1 + len(end_target): len(string)].find(end_target) + len(end_target)
        end = end1 + end2

        # Add the sub string to result and set-up for the next loop.
        result.append(string[0: end])
        string = string[end + len(end_target): len(string)]
        start = string.find(start_target)
    return result

# -------------------------------------------------- Part: Extraction/Substitution Methods


# Extract all cases of a given target (exclusive) from a given string.
# For example if this method is called on the following string:
#           string = substring_1 + target + substring_2 + target
# This method will return substring_1 + substring_2
def extract(string, target):
    # As long as the target can be found do...
    start = string.find(target)
    while start != -1:
        start_string = string[0: start]
        end_string = string[start + len(target): len(string)]
        string = start_string + end_string
        start = string.find(target)
    return string


# Extract in all cases everything between a given start_target (exclusive)
# to a given end_target (exclusive) from a given string.
# For example if this method is called on the following string:
#           string = start_target + substring_1 + end_target target + substring_2
# This method will return substring_2
def extract_between(string, start_target, end_target):
    start = string.find(start_target)
    while start != -1:
        start_string = string[0: start]
        end = string.find(end_target)
        if end == -1:
            return string
        string = start_string + string[end + len(end_target): len(string)]
        start = string.find(start_target)
    return string


# Extract everything of the first html link tag from a given string.(<a href="...">text</a>) except it's text.
# For example if this method is called on the following string:
#           string = substring_1 + <a href="...">text</a> + substring_2 + <a href="...">text</a>
# This method will return substring_1 + text + substring_2 + <a href="...">text</a>
def extract_text_from_link_tag(string):
    start_target = "<a href=\""
    og_start = string.find(start_target)
    if og_start == -1:
        return string

    user = string[og_start: len(string)]
    start_target = "\">"
    start = og_start + user.find(start_target)
    end_target = "</a>"
    end = og_start + user.find(end_target)

    return string[0: og_start] + string[start + len(start_target): end] + string[end + len(end_target): len(string)]


# def extract_title_from_link_tag(string):
#     start_target = "<a href=\""
#     og_start = string.find(start_target)
#     if og_start == -1:
#         return string
#
#     user = string[og_start : len(string)]
#     start_target = "title=\""
#     start = og_start + user.find(start_target)
#     end_target = "\""
#     end = og_start + user.find(end_target)
#
#     og_end = user.find("</a>") + len("</a>")
#     return string[0: og_start] + string[start: end] + string[og_end: len(string)]


# Substitute all the cases of a given original target with given new targets.
# For example if this method is called on the following string:
#           string = text + og_target + text + og_target + text
# This method will return text + new_target + text + new_target + text
def substitute(string, og_target, new_target):
    start = string.find(og_target)
    while start != -1:
        start_string = string[0: start]
        end_string = string[start + len(og_target): len(string)]
        string = start_string + new_target + end_string
        start = string.find(og_target)
    return string


# Extract all the garbage from a given filtered html output made in the main method of this program.
# NOTE: See Implementation.
# FIXME: Update is necessary if wikipedia switches it's syntax.
# FIXME: Add more extract/substitute tasks.
def extract_garbage(output):
    extract_tasks = ["</td>", "<td style=\"vertical-align:top\">", "\"", "\n",
                     "<span style=font-size:85%>", "</span>", "</span"]
    substitute_tasks = [[" / ", " "], [" : ", " "], ["&amp;", "&"]]
    for i in range(len(output)):
        string = output[i]
        # Before extracting all cases of: ", all the link tags are handled, this ordering is necessary
        # due to the implementation of extract_text_from_link_tag.
        old_string = ""
        while old_string != string:
            old_string = string
            string = extract_text_from_link_tag(string)

        # Extract all the extract tasks
        for j in range(len(extract_tasks)):
            string = extract(string, extract_tasks[j])
        # Substitute all the extract tasks
        for j in range(len(substitute_tasks)):
            string = substitute(string, substitute_tasks[j][0], substitute_tasks[j][1])

        # Update output
        output[i] = string
    return output

# -------------------------------------------------- Part: General Tag Methods


# If possible, converts a given genre to the normalized version of this genre.
# For example if the genre is Conscious hip hop, this method will return Hip-Hop.
# FIXME: Add more normalizations.
def lookup_normalized_genre(genre):
    if genre == "Hip hop":
        return "Hip-Hop"
    elif genre == "Conscious hip hop":
        return "Hip-Hop"
    elif genre == "West Coast hip hop":
        return "Hip-Hop"
    else:
        return genre


# If possible, converts a given publisher to the normalized version of this publisher.
# For example if the publisher is Visionary Music Group, this method will return Visionary.
# FIXME: Add more normalizations.
def lookup_normalized_publisher(publisher):
    if publisher == "Visionary Music Group":
        return "Visionary"
    else:
        return publisher


# Assign the general tags by using the values found in the file located at the given path.
def assign_gen_tags(path):
    file = open(path, "r")
    gen_tags = file.readlines()
    file.close()

    # The file needs to use the correct syntax.
    if len(gen_tags) != 6:
        raise SyntaxError

    # Get rid of all trailing newline characters.
    for i in range(len(gen_tags)):
        gen_tags[i] = gen_tags[i].rstrip()
    return gen_tags


# Extract all the garbage from a given filtered string output made in the infer_gen_tags method of this program.
# NOTE: See Implementation.
# FIXME: Update is necessary if wikipedia switches it's syntax.
# FIXME: Add more extract/substitute tasks.
def infer_gen_tags_extract_garbage(string):
    extract_tasks = ["\"", "\n"]
    extract_between_tasks = [["<sup", "</sup>"]]
    substitute_tasks = [["&amp;", "&"]]

    for i in range(len(extract_tasks)):
        string = extract(string, extract_tasks[i])
    for i in range(len(extract_between_tasks)):
        string = extract_between(string, extract_between_tasks[i][0], extract_between_tasks[i][1])
    for i in range(len(substitute_tasks)):
        string = substitute(string, substitute_tasks[i][0], substitute_tasks[i][1])

    return string


# Helper method of infer_gen_tags, this method will return the publisher of the album
# at the given wikipedia link specified by the user.
def infer_gen_tags_publisher(html):
    start_target = "title=\"Record label\">Label</a></th>\n<td class=\"hlist\">"
    string = get_substrings_between(html, start_target, "</td>")
    try:
        string = extract_text_from_link_tag(get_substrings_between(string, "<li>", "</li>"))
    except LookupError:
        string = extract_text_from_link_tag(string)
        try:
            string = string[0] + get_substrings_between(string, string[0], ", ")
        except LookupError:
            string = string
    return string


# Helper method of infer_gen_tags, this method will return the genre of the album
# at the given wikipedia link specified by the user
def infer_gen_tags_genre(html):
    start_target = "<th scope=\"row\"><a href=\"/wiki/Music_genre\" title=\"Music genre\">Genre</a></th>\n" + \
                   "<td class=\"category hlist\">"
    string = get_substrings_between(html, start_target, "</td>")
    try:
        string = extract_text_from_link_tag(get_substrings_between(string, "<li>", "</li>"))
    except LookupError:
        string = extract_text_from_link_tag(string)
        try:
            string = string[0] + get_substrings_between(string, string[0], ", ")
        except LookupError:
            string = string
    return string


# Infer the general (for the entire album) tags by using the html document
# of the given wikipedia link specified by the user.
def infer_gen_tags(html):
    gen_tags = ["artist", "album", "genre", "publisher", "year", "False"]

    # Get the album artist.
    string = get_substrings_between(html, " by <span class=\"contributor\">", "</span>")
    gen_tags[0] = extract_text_from_link_tag(string)

    # Get the album name.
    gen_tags[1] = get_substrings_between(html, "<p><i><b>", "</b></i>")

    # Get the album genre.
    try:
        gen_tags[2] = lookup_normalized_genre(infer_gen_tags_extract_garbage(infer_gen_tags_genre(html)))
    except LookupError:
        gen_tags[2] = ""

    # Get the album publisher
    try:
        gen_tags[3] = lookup_normalized_publisher(infer_gen_tags_extract_garbage(infer_gen_tags_publisher(html)))
    except LookupError:
        gen_tags[3] = ""

    # Get the album year
    start_target = "<td style=\"width: 33%; text-align: center; vertical-align: top; padding: .2em .1em\">"
    start = html.find(start_target)
    string = html[start: len(html)]
    gen_tags[4] = get_substrings_between(string, "<br />\n", ")")
    gen_tags[4] = extract(gen_tags[4], "(")
    return gen_tags

# -------------------------------------------------- Part: Specific Tag Methods


# Helper method of generate_spec_tags, this method will normalize the featuring artist part of a given string.
# For example if this method is called on the following string:
#           string = " (featuring Black Thought, Chuck D, Big Lenbo and No I.D.)"
# This method will return Black Thought;Chuck D;Big Lenbo;No I.D.
def generate_spec_tags_features(string):
    target = " (featuring "
    if string.find(target) == -1:
        return string

    string = extract(string, target)
    string = extract(string, ")")
    string = substitute(string, " and ", ";")
    string = substitute(string, ", ", ";")
    return string


# Generates the data for the specific tags of individual songs (title, track_num, artists).
# All these tags are specific for each individual song of an album because all the other tags (non-specific)
# apply to the entire album, specific tags are different for each song.
def generate_spec_tags(output, gen_tags):
    spec_tags = list()
    for i in range(len(output)):
        temp = ["title", "track_num", "artists"]
        string = output[i]
        pivot1 = string.find(".")
        temp[1] = string[0: pivot1]

        pivot2 = string.find(" (featuring ")
        # If there are no featured artists:
        if pivot2 == -1:
            temp[0] = string[pivot1 + 1: len(string)]
            temp[2] = gen_tags[0]
        # Else there are featured artists:
        else:
            temp[0] = string[pivot1 + 1: pivot2]
            temp[2] = string[pivot2: len(string)]
            temp[2] = gen_tags[0] + ";" + generate_spec_tags_features(temp[2])

        spec_tags.append(temp)
    return spec_tags

# -------------------------------------------------- Part: Assign id3 Tags Methods.


# Assign the id3 tags of the .mp3 files of songs in the given album located in this program's directory
# to the found specific and general tag values.
def assign_id3_tags(spec_tags, gen_tags):
    artist = gen_tags[0]
    album = gen_tags[1]
    genre = gen_tags[2]
    publisher = gen_tags[3]
    year = int(gen_tags[4])
    debug = gen_tags[5]

    for spec_tag in spec_tags:
        title = spec_tag[0]
        number = int(spec_tag[1])
        all_artists = spec_tag[2]
        # If the file exists, assign id3 tags, else continue
        try:
            # print(artist + " - " + title + ".mp3")
            audio_file = eyed3.load(artist + " - " + title + ".mp3")
        except IOError:
            continue

        audio_file.tag.title = title
        audio_file.tag.comments.set(u"")
        audio_file.tag.artist = all_artists
        audio_file.tag.album_artist = artist
        audio_file.tag.album = album
        audio_file.tag.track_num = number
        audio_file.tag.genre = genre
        audio_file.tag.publisher = publisher

        audio_file.tag.release_date = eyed3.core.Date(year)
        audio_file.tag.orig_release_date = eyed3.core.Date(year)
        audio_file.tag.recording_date = eyed3.core.Date(year)
        # audio_file.tag.encoding_date = eyed3.core.Date(year)
        # audio_file.tag.tagging_date = eyed3.core.Date(year)

        audio_file.tag.save()

        # Only print confirmation if the user specified debugging.
        if debug == "True":
            print(audio_file.tag.title)
            print(audio_file.tag.artist)
            print(audio_file.tag.album_artist)
            print(audio_file.tag.album)
            print(audio_file.tag.track_num)
            print(audio_file.tag.genre)
            print(audio_file.tag.publisher)
    return

# -------------------------------------------------- Part: Main Method and global variables.


# Main method.
# FIXME: Update is necessary if wikipedia switches it's syntax.
def main():
    del[sys.argv[0]]

    if dev_mode:
        sys.argv.append("https://en.wikipedia.org/wiki/Under_Pressure_(album)")
        # sys.argv.append("test_rules.txt")

    # Get and decode the html file located at the given wikipedia page
    html = urllib.request.urlopen(sys.argv[0]).read()
    html = html.decode("utf-8")

    # Infer or Assign the general tags depending upon the amount of command line arguments.
    if len(sys.argv) < 2:
        gen_tags = infer_gen_tags(html)
    else:
        gen_tags = assign_gen_tags(sys.argv[1])

    # Construct the search targets.
    color1 = "<tr style=\"background-color:#fff\">\n"
    color2 = "<tr style=\"background-color:#f7f7f7\">\n"
    start_garbage = "<td style=\"padding-right:10px;text-align:right;vertical-align:top\">"
    end_target = "</td>\n"

    # Combine the raw outputs of the two colors.
    list1 = get_all_substrings_between(html, color1 + start_garbage, end_target)
    list2 = get_all_substrings_between(html, color2 + start_garbage, end_target)
    output = list1 + list2
    # print(output)

    # Transform and Assign the raw output.
    output = extract_garbage(output)
    output = generate_spec_tags(output, gen_tags)
    if dev_mode:
        print(gen_tags)
        for item in output:
            print(item)
    assign_id3_tags(output, gen_tags)
    return


dev_mode = False
main()
