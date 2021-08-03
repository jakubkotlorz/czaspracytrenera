from datetime import date, datetime
from django.db.models import manager
from .models import Employment, Team


class ParserError(Exception):
    """Base class for parser's exceptions."""
    pass


class NotEnoughColumnsError(ParserError):
    """Raised when not enough of columns to be parsed."""
    pass

class CannotFindDateError(ParserError):
    """Raised when cannot find date."""
    pass


class ParsedEmployment:
    def __init__(self, input_line, manager):
        self.manager = manager
        fields = input_line.split('\t')
        if len(fields) < 4:
            raise NotEnoughColumnsError
        self.teamText = fields[0]
        self.teamChooseList = Team.search_team(fields[0])
        self.start, self.finish = self.validData(fields)


    def getEmployment(self):
        current = True
        return Employment(
            manager=self.manager, 
            #team=team, 
            # date_start=start, 
            # date_finish=finish, 
            # still_hired=current, 
            # role='First'
        )

    def validData(self, fields):
        # try to find first table column with a date
        for col in [1, 2, 3]:
            try:
                dateFrom = self.dateFromString(fields[col])
                dateTo = self.dateFromString(fields[col+1]) if fields[col+1].lower() != 'present' else None
                return dateFrom, dateTo
            except ValueError:
                # continue if not a date
                pass
        raise CannotFindDateError

    def dateFromString(self, dateString):
        return datetime.strptime(dateString, '%d %B %Y').date()


class WikiTableParser:
    def __init__(self, inputForm, manager) -> None:
        self.jobs = list()
        tableData =  inputForm['wikiInput'].split('\n')
        for entry in tableData:
            try:
                self.jobs.append(ParsedEmployment(entry, manager))
            except NotEnoughColumnsError:
                print("Not enough columns in this line:", entry)
            except CannotFindDateError:
                print("Cannot find date in this line:", entry)
            except:
                print("Cannot process this line:", entry)


    def checkIfPeriodsOverlap(self, parsedStart, parsedEnd, storedPeriods):
        for stored in storedPeriods:
            if parsedStart == stored[0] or parsedEnd == stored[1]:
                # print(parsedStart, parsedEnd, stored[0], stored[1])
                return True
        return False

    def markIntroducedJobs(self, storedPeriods):
        for parsedJob in self.jobs:
            # print("AAAAAAAAAAAAAA:", parsedJob.teamText)
            parsedJob.saved = True if self.checkIfPeriodsOverlap(parsedJob.start, parsedJob.finish, storedPeriods) else False
            


    def getAllJobs(self):
        return self.jobs
