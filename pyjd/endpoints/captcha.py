from pyjd.endpoints import Action
from pyjd.jd_types import CaptchaJob, SkipRequest


class Captcha(Action, endpoint="captcha"):
    def get(self, captcha_id: int, c_format: str | None = None) -> str:
        """Get the base64 captcha image.

        The result is a captcha image as base64 encoded data url.

        :param captcha_id: The ID of the captcha.
        :type captcha_id: int
        :param format: The format
        :type format: str
        :return: Captcha image (base64 encoded).
        :rtype: str
        """

        params = [str(captcha_id)]
        if c_format:
            params.append(c_format)
        return self.action("/get", params, binary=True)

    def get_captcha_job(self, job_id: int) -> CaptchaJob:
        """Get a captcha job for `job_id`

        :param job_id: ID of the job
        :type job_id: int
        :return: The captcha job object
        :rtype: CaptchaJob
        """

        params = [job_id]
        resp = self.action("/getCaptchaJob", params)
        captcha_job = CaptchaJob(**resp)
        return captcha_job

    def list(self) -> list[CaptchaJob]:
        """Get the waiting captchas

        :return: Returns a list of all available captcha jobs
        :rtype: List[CaptchaJob]
        """

        resp = self.action("/list", None)
        captcha_jobs = []
        for job in resp:
            captcha_job = CaptchaJob(**job)
            captcha_jobs.append(captcha_job)

        return captcha_jobs

    def skip(self, captcha_id: int, skip_type: SkipRequest = SkipRequest.SINGLE) -> bool:
        """Skip a captcha with a SkipRequest type

        :param captcha_id: ID of the captcha to skip
        :type captcha_id: int
        :param skip_type: The SkipRequest type
        :type skip_type: jd_types.SkipRequest
        :return: Success
        :rtype: boolean
        """

        params = [captcha_id, skip_type.value]
        resp = self.action("/skip", params)
        return resp

    def solve(self, captcha_id: int, result: str, result_format: str | None = None) -> bool:
        """Solve a captcha.

        :param captcha_id: The ID of the captcha that is solved.
        :type captcha_id: int
        :param result: The solution of the captcha.
        :type result: str
        :param result_format: Format of the result
        :type result_format: str
        :return: Success
        :rtype: boolean
        """

        params = [captcha_id, result]
        if result_format:
            params.append(result_format)
        resp = self.action("/solve", params)
        return resp
