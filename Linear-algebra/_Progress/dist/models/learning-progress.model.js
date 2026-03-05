export class LearningProgressModel {
    _id;
    ticketId;
    numberTicket;
    theme;
    text;
    understandingStatus;
    attemptCount;
    lastAttemptDate;
    constructor(_id, ticketId, numberTicket, theme, text, understandingStatus, attemptCount, lastAttemptDate) {
        this._id = _id;
        this.ticketId = ticketId;
        this.numberTicket = numberTicket;
        this.theme = theme;
        this.text = text;
        this.understandingStatus = understandingStatus;
        this.attemptCount = attemptCount;
        this.lastAttemptDate = lastAttemptDate;
    }
    toJSON() {
        return {
            _id: this._id,
            ticketId: this.ticketId,
            numberTicket: this.numberTicket,
            theme: this.theme,
            text: this.text,
            understandingStatus: this.understandingStatus,
            attemptCount: this.attemptCount,
            lastAttemptDate: this.lastAttemptDate,
        };
    }
    static fromJSON(data) {
        return new LearningProgressModel(data._id, data.ticketId, data.numberTicket, data.theme, data.text, data.understandingStatus, data.attemptCount, data.lastAttemptDate);
    }
}
