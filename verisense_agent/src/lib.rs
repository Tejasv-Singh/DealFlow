use scale_info::TypeInfo;
use vrs_core_sdk::codec::{Decode, Encode};
use vrs_core_sdk::nucleus;

#[derive(Debug, Decode, Encode, TypeInfo)]
pub struct User {
    pub id: u64,
    pub name: String,
}

#[nucleus]
pub mod nucleus {
    use crate::User;
    use vrs_core_sdk::codec::{Decode, Encode};
    use vrs_core_sdk::{get, post, storage};

    #[post]
    pub fn add_user(user: User) -> Result<u64, String> {
        let key = [&b"user:"[..], &user.id.to_be_bytes()[..]].concat();
        println!("{:?}", key);
        storage::put(&key, &user.encode()).map_err(|e| e.to_string())?;
        Ok(user.id)
    }

    #[get]
    pub fn get_user(id: u64) -> Result<Option<User>, String> {
        let key = [&b"user:"[..], &id.to_be_bytes()[..]].concat();
        println!("{:?}", key);
        let result = storage::get(&key).map_err(|e| e.to_string())?;
        let user = result.map(|data| User::decode(&mut &data[..]).unwrap());
        Ok(user)
    }
}
