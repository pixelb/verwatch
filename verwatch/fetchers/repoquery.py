from verwatch.fetch import VersionFetcher
from verwatch.util import run, parse_nvr


class RepoqueryFetcher(VersionFetcher):
    name = 'repoquery'

    def __init__(self, paths=None, options=None):
        if not options or 'repo_base' not in options:
            raise ValueError("'repo_base' option not supplied to repoquery fetcher.")
        self.paths = paths
        self.repo_base = options['repo_base']

    def get_version(self, pkg_name, branch):
        errc, out, err = run("repoquery --repofrompath=_repo_,%(repo_base)s/%(branch)s/ --repoid=_repo_ -q %(pkg_name)s" % {
                             'repo_base': self.repo_base,
                             'branch': branch,
                             'pkg_name': pkg_name})
        if errc:
            return {'error': err or out}
        if not out:
            return {'error': "No version found."}
        lines = out.strip().split("\n")
        if len(lines) > 1:
            # TODO: Select best version.
            raise NotImplementedError("Got more than 1 version using repoquery... FIXME!")
        return parse_nvr(lines[0], pkg_name)