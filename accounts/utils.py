def normalize_email(email):
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError as e:
        raise ValueError(e.args)
    else:
        email = email_name + '@' + domain_part.lower()
    return email
