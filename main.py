import argparse

from python_hosts import Hosts, HostsEntry

BEGIN_COMMENT = '# blocksite:begin'
END_COMMENT = '# blocksite:end'

parser = argparse.ArgumentParser(description='blocksite')
parser.add_argument('hosts_path', type=str,
                    help='Path to hosts file')
parser.add_argument('sites_file', type=str,
                    help='Path to sites file')
parser.add_argument('--disable', action='store_true', help='Enable or disable block')

if __name__ == '__main__':
    args = parser.parse_args()

    sites = set([])
    with open(args.sites_file) as sites_file:
        for site in sites_file.readlines():
            site = site.strip()
            if site.startswith('#') or len(site) == 0:
                continue
            sites.add(site)

    hosts = Hosts(path=args.hosts_path)

    # Clear
    removing = False
    new_entries = []
    for entry in hosts.entries:
        if entry.comment == BEGIN_COMMENT:
            removing = True
        elif entry.comment == END_COMMENT:
            removing = False
        elif not removing:
            new_entries.append(entry)
    hosts.entries = new_entries

    # Add entries
    if not args.disable:
        entries = [HostsEntry(entry_type='comment', comment=BEGIN_COMMENT)]
        for site in sites:
            entries.append(HostsEntry(entry_type='ipv4', address='127.0.0.1', names=[site]))
        entries.append(HostsEntry(entry_type='comment', comment=END_COMMENT))
        hosts.add(entries)

    hosts.write()