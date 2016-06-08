import mimetypes

import re

file_type_by_mime = {
    'application/postscript': 'postscript',
    'application/pdf': 'pdf',
    'application/msword': 'ms_word',
    re.compile('^'+re.escape('application/vnd.ms-word')): 'ms_word',
    re.compile('^'+re.escape('application/vnd.ms-excel')): 'ms_excel',
    re.compile('^'+re.escape('application/vnd.ms-powerpoint')): 'ms_powerpoint',
    re.compile('^'+re.escape('application/vnd.openxmlformats-officedocument.spreadsheetml.')): 'ms_excel',
    re.compile('^'+re.escape('application/vnd.openxmlformats-officedocument.presentationml')): 'ms_powerpoint',
    re.compile('^'+re.escape('application/vnd.openxmlformats-officedocument.wordprocessingml')): 'ms_word',

    re.compile('^image/'): 'image',
    re.compile('^video/'): 'video',
}

file_type_names = {
    'default': 'File',
    'ms_word': 'Document',
    'ms_excel': 'Document',
    'ms_powerpoint': 'Presentation',
    'pdf': 'PDF',
    'image': 'Image',
    'video': 'Video',
}


def get_file_type(filename):
    """
    Guess file type by mime.
    """
    mime_type, encoding = mimetypes.guess_type(filename, strict=False)
    file_type = None
    for mime_type_test in file_type_by_mime:
        if not isinstance(mime_type_test, basestring):
            if mime_type_test.match(mime_type):
                file_type = file_type_by_mime[mime_type_test]
                break
        else:
            if mime_type_test == mime_type:
                file_type = file_type_by_mime[mime_type_test]
                break

    return file_type


def get_file_type_name(file_type):
    """
    Get file type verbose.
    """
    return file_type_names.get(file_type, file_type_names['default'])
