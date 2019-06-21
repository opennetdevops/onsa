import * as yup from "yup";

export const validationSchema = () => {
  const minId = 6;
  const maxId = 20;
  const minBw = 1;
  const maxBw = 1024;
  const minPrefix = 24;
  const maxPrefix = 32;
  const idErr =
    "The IDs field must be between " +
    minId +
    " and " +
    maxId +
    " characters long.";
  const bwErr =
    "The Bandwidth must be an integer number between " +
    minBw +
    " and " +
    maxBw +
    ".";
  const prefixErr =
    "The Prefix must be an integer number between " +
    minPrefix +
    " and " +
    maxPrefix +
    ".";

  yup.setLocale({
    string: { trim: "Check for leading and trailling spaces." }
  });

  let selectSchema = yup.string().required();
  let idSchema = yup
    .string()
    .strict(true)
    .trim()
    .min(minId, idErr)
    .max(maxId, idErr)
    .required();

  let schema = yup.object({
    client: selectSchema.label("Client"),
    custLoc: selectSchema.label("Customer Location"),
    servType: selectSchema.label("Service Type"),
    hub: selectSchema.label("Hub"),
    id: idSchema,
    gts_id: idSchema,
    bandwidth: yup
      .number()
      .typeError(bwErr)
      .min(minBw, bwErr)
      .max(maxBw, bwErr)
      .integer(bwErr)
      .positive(bwErr)
      .required(bwErr),
    prefix: yup
      .number()
      .typeError(prefixErr)
      .min(minPrefix, prefixErr)
      .moreThan(minPrefix, prefixErr)
      .max(maxPrefix, prefixErr)
      .integer(prefixErr)
      .positive(prefixErr)
      .when("$showPrefix", (showPrefix, schema) =>
        showPrefix ? schema.required(prefixErr) : schema.notRequired()
      ),
    access_port_id: selectSchema
      .label("Port")
      .when("$showPort", (showPort, schema) =>
        showPort ? schema.required() : schema.notRequired()
      )
  });
  return schema;
};
