"""Token.py: To store the tokens read from the file which is used to build further len1,2,3,4,..
tokens for information extraction."""

__author__ = "Ankit Maharia"

TAG_START_IDENTIFIER = "<Entity>"
TAG_END_IDENTIFIER = "</Entity>"


class Token:
    label = None  # 0 for false
    name = None
    documentId = None
    startPosition = None
    endPosition = None
    lineNumber = None
    hasStartTag = None
    hasEndTag = None
    hasBefore = None
    hasAfter = None
    endTagCount = 0
    startTagCount = 0
    content_index = None

    starts_with_quotes = None
    ends_with_quotes = None
    ends_with_apostrophes = None
    ends_with_dot = None
    ends_with_comma = None

    def __init__(self, name, document_id, line_number, startPosition, endPosition, hasBefore, hasAfter, content_index):
        self.name = Token.__sanitized_name(name)
        self.documentId = document_id
        self.startPosition = startPosition
        self.endPosition = endPosition
        self.lineNumber = line_number
        self.hasStartTag = Token.__has_start_tag(name)
        self.hasEndTag = Token.__has_end_tag(name)
        if self.hasEndTag:
            self.endTagCount = 1
        if self.hasStartTag:
            self.startTagCount = 1
        self.label = self.hasStartTag and self.hasEndTag
        self.hasBefore = hasBefore
        self.hasAfter = hasAfter
        self.content_index = content_index
        self.__tag_shift()

    def update(self, token):
        self.name = self.name + ' ' + token.name
        self.endPosition = token.endPosition
        if token.hasStartTag:
            self.startTagCount += 1
        if token.hasEndTag:
            self.endTagCount += 1
            self.label = self.hasStartTag and self.startTagCount == 1 and self.endTagCount == 1
        else:
            self.label = False
        self.hasAfter = token.hasAfter

    def __tag_shift(self):
        """
        Because of the tags introduced the column number needs to be shifted to what it was in the actual text doc.
        This is introduced so that parse can use the method to shift the value
        """
        delta = 0
        if self.hasStartTag:
            inc = Token.__start_tag_length()
            self.startPosition = self.startPosition - inc
            self.endPosition = self.endPosition - inc
            delta = delta + inc
        if self.hasEndTag:
            inc = Token.__end_tag_length()
            self.endPosition = self.endPosition - inc
            delta = delta + inc

    @staticmethod
    def __has_start_tag(name):
        # type: (str) -> bool
        """

        :param name: String to check if has the start tag of the manual tagging done
        :return: true if yes, false otherwise
        """
        return name.startswith(TAG_START_IDENTIFIER)

    @staticmethod
    def __start_tag_length():
        # type: () -> int
        """

        :return: Length of the start tag used in manual tagging
        """
        return len(TAG_START_IDENTIFIER)

    @staticmethod
    def __has_end_tag(name):
        # type: (str) -> bool
        """

        :param name: string to check if it end with the end tag of positive label
        :return: true if yes and false if no
        """
        return name.endswith(TAG_END_IDENTIFIER)

    @staticmethod
    def __end_tag_length():
        # type: () -> int
        """

        :return: Length of the end tag when manual tagging was done for positive labels
        """
        return len(TAG_END_IDENTIFIER)

    @staticmethod
    def is_positive(name):
        # type: (str) -> bool
        """

        :param name: A string to check if it has the tags which identifies a positive label
        :return: true if yes false if no
        """
        return Token.__has_start_tag(name) and Token.__has_end_tag(name)

    @staticmethod
    def __sanitized_name(name):
        rv = name
        if Token.__has_start_tag(rv):
            rv = rv[Token.__start_tag_length():]
        if Token.__has_end_tag(rv):
            rv = rv[0:len(rv) - Token.__end_tag_length()]
        return rv

    @staticmethod
    def clone(token):
        # type: (Token) -> Token
        """

        :param token: token to clone
        :return: new token created with sanitized name
        """
        tok = Token(token.name, token.documentId, token.lineNumber, token.startPosition,
                    token.endPosition, token.hasBefore, token.hasAfter, token.content_index)
        tok.hasStartTag = token.hasStartTag
        tok.hasEndTag = token.hasEndTag
        tok.endTagCount = token.endTagCount
        tok.startTagCount = token.startTagCount
        tok.label = token.label
        return tok
